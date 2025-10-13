import os
import json
import time
import winreg
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from utils.IconUtils import get_icon_path
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    try:
        return QCoreApplication.translate("InterfaceGerenciadorAtividades", text)

    except Exception:
        return text

class TrialManager:
    CONFIG_FILE = "trial_info.json"
    DEFAULT_TRIAL = "minutes"  # Pode ser "minutes" ou "days"
    DEFAULT_TRIAL_VALUE = 1    # Valor inteiro para minutos ou dias
    PAID_VERSION_URL = "ms-windows-store://pdp/?productid=9P289X0185C3"
    LIBERAR_USO_DEFINITIVO = False  # Altere para True para liberar uso definitivo
    REG_PATH = r"SOFTWARE\EisenhowerOrganizer"
    REG_KEY = "FirstRunTimestamp"

    @classmethod
    def get_config_path(cls):
        try:
            config_dir = obter_caminho_persistente()
            return os.path.join(config_dir, cls.CONFIG_FILE)

        except Exception as e:
            logger.error(f"Erro ao obter caminho de configuração: {e}")
            return None

    @classmethod
    def get_first_run_timestamp(cls):
        try:
            views = [
                winreg.KEY_READ | getattr(winreg, "KEY_WOW64_64KEY", 0),
                winreg.KEY_READ | getattr(winreg, "KEY_WOW64_32KEY", 0),
                winreg.KEY_READ
            ]
            for access in views:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, access) as key:
                        value, val_type = winreg.QueryValueEx(key, cls.REG_KEY)
                        if isinstance(value, int):
                            return int(value)

                        try:
                            return int(str(value))

                        except Exception:
                            logger.debug(f"Valor do registro não é inteiro: {value} (type={val_type})")
                            return None

                except FileNotFoundError:
                    continue

                except OSError as e:
                    logger.debug(f"Falha ao abrir chave do registro (access={access}): {e}")
                    continue

            return None

        except Exception as e:
            logger.error(f"Erro inesperado ao obter timestamp do registro: {e}", exc_info=True)
            return None

    @classmethod
    def set_first_run_timestamp(cls, timestamp):
        try:
            views = [
                winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY if hasattr(winreg, "KEY_WOW64_64KEY") else winreg.KEY_WRITE,
                winreg.KEY_WRITE | winreg.KEY_WOW64_32KEY if hasattr(winreg, "KEY_WOW64_32KEY") else winreg.KEY_WRITE,
                winreg.KEY_WRITE
            ]
            for access in views:
                try:
                    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, access) as key:
                        try:
                            winreg.SetValueEx(key, cls.REG_KEY, 0, winreg.REG_DWORD, int(timestamp))

                        except Exception:
                            winreg.SetValueEx(key, cls.REG_KEY, 0, winreg.REG_SZ, str(timestamp))

                        return

                except OSError as e:
                    logger.debug(f"Falha ao criar/abrir chave para gravar (access={access}): {e}")
                    continue

            logger.error("Não foi possível gravar timestamp no registro com nenhuma visão disponível.")

        except Exception as e:
            logger.error(f"Erro ao definir timestamp no registro: {e}", exc_info=True)

    @classmethod
    def delete_first_run_timestamp(cls):
        try:
            removed = False
            views = [
                winreg.KEY_ALL_ACCESS | getattr(winreg, "KEY_WOW64_64KEY", 0),
                winreg.KEY_ALL_ACCESS | getattr(winreg, "KEY_WOW64_32KEY", 0),
                winreg.KEY_ALL_ACCESS
            ]
            for access in views:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, access) as key:
                        try:
                            winreg.DeleteValue(key, cls.REG_KEY)
                            logger.info(f"Timestamp removido do registro (access={access}).")
                            removed = True

                        except FileNotFoundError:
                            continue

                        except OSError as e:
                            logger.debug(f"Não foi possível remover valor nesta visão (access={access}): {e}")
                            continue

                    if removed:
                        break

                except FileNotFoundError:
                    continue

                except OSError as e:
                    logger.debug(f"Falha ao abrir chave do registro para remoção (access={access}): {e}")
                    continue

            if not removed:
                logger.warning("Timestamp não encontrado no registro em nenhuma visualização; tentando remover chave inteira se existir.")
                try:
                    if hasattr(winreg, "DeleteKeyEx"):
                        try:
                            winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, 0)
                            logger.info("Chave do registro removida com DeleteKeyEx.")

                        except OSError as e:
                            logger.debug(f"Não foi possível remover chave com DeleteKeyEx: {e}")

                    else:
                        try:
                            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH)
                            logger.info("Chave do registro removida com DeleteKey.")

                        except OSError as e:
                            logger.debug(f"Não foi possível remover chave com DeleteKey: {e}")

                except Exception as e:
                    logger.debug(f"Tentativa de remoção da chave inteira falhou: {e}")

        except Exception as e:
            logger.error(f"Erro ao remover timestamp do registro: {e}", exc_info=True)

        try:
            path = cls.get_config_path()
            if path and os.path.exists(path):
                os.remove(path)
                logger.info(f"Arquivo de configuração do trial removido: {path}")

        except Exception as e:
            logger.error(f"Erro ao remover arquivo de configuração do trial: {e}", exc_info=True)

    @classmethod
    def get_trial_info(cls):
        try:
            path = cls.get_config_path()
            first_run = cls.get_first_run_timestamp()

            if path and os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        info = json.load(f)
                        if first_run is not None:
                            info["first_run"] = first_run

                        else:
                            cls.set_first_run_timestamp(info.get("first_run", int(time.time())))

                        return info

                except Exception as e:
                    logger.error(f"Erro ao ler arquivo de configuração: {e}")

            timestamp = first_run if first_run is not None else int(time.time())
            info = {"first_run": timestamp}
            if path:
                try:
                    with open(path, "w") as f:
                        json.dump(info, f)

                except Exception as e:
                    logger.error(f"Erro ao criar arquivo de configuração: {e}")

            if first_run is None:
                cls.set_first_run_timestamp(timestamp)

            return info

        except Exception as e:
            logger.error(f"Erro geral em get_trial_info: {e}")
            return {"first_run": int(time.time())}

    @classmethod
    def is_trial_expired(cls):
        try:
            info = cls.get_trial_info()
            first_run = info.get("first_run", int(time.time()))
            now = int(time.time())
            if cls.DEFAULT_TRIAL == "minutes":
                trial_seconds = cls.DEFAULT_TRIAL_VALUE * 60

            elif cls.DEFAULT_TRIAL == "days":
                trial_seconds = cls.DEFAULT_TRIAL_VALUE * 24 * 3600

            else:
                trial_seconds = 0

            return (now - first_run) > trial_seconds

        except Exception as e:
            logger.error(f"Erro ao verificar expiração do trial: {e}")
            return False

    @classmethod
    def enforce_trial(cls, parent=None):
        try:
            if cls.LIBERAR_USO_DEFINITIVO:
                return

            if cls.is_trial_expired():
                msg = QMessageBox(parent)
                icon_file = get_icon_path("ReviewsManager.ico")
                msg.setWindowIcon(QIcon(icon_file))
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle(get_text("trial_expired_title"))
                msg.setTextFormat(Qt.TextFormat.RichText)
                msg.setText(
                    f"{get_text('trial_expired_message')}<br>"
                    f"{get_text('trial_buy_message')}<br><br>"
                    f"{get_text('trial_uninstall_message')}<br><br>"
                    f'<a href="{cls.PAID_VERSION_URL}">{get_text('trial_paid_link')}</a>'
                )
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                os._exit(0)

        except Exception as e:
            logger.error(f"Erro ao aplicar restrição do trial: {e}")
