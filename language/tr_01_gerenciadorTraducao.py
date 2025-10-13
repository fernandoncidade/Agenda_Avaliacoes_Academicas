import os
import sys
import json
from PySide6.QtCore import QTranslator, QCoreApplication, Signal, QObject
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class GerenciadorTraducao(QObject):
    idioma_alterado = Signal(str)
    
    def __init__(self):
        super().__init__()
        try:
            self.tradutor = None
            self.idioma_atual = "pt_BR"
            self.app = QCoreApplication.instance()
            self.idioma_padrao = "pt_BR"

            self.idiomas_disponiveis = {
                "pt_BR": "Português (Brasil)",
                "en_US": "English (United States)"
            }

            self.dir_traducoes = os.path.join(
                getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
                "language", "translations"
            )

            os.makedirs(self.dir_traducoes, exist_ok=True)
            self.carregar_configuracao_idioma()

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorTraducao: {e}", exc_info=True)

    def carregar_configuracao_idioma(self):
        config_path = self.obter_caminho_configuracao()
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'idioma' in config:
                        self.idioma_atual = config['idioma']

        except Exception as e:
            logger.error(f"Erro ao carregar configuração de idioma: {e}", exc_info=True)

    def salvar_configuracao_idioma(self):
        config_path = self.obter_caminho_configuracao()
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            config = {'idioma': self.idioma_atual}
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Erro ao salvar configuração de idioma: {e}", exc_info=True)

    def obter_caminho_configuracao(self):
        try:
            persist_dir = obter_caminho_persistente()
            return os.path.join(persist_dir, 'language.json')

        except Exception as e:
            logger.error(f"Erro ao obter caminho de configuração: {e}", exc_info=True)

    def _remover_tradutor_instalado(self):
        try:
            app = self.app or QCoreApplication.instance()
            trad_instalado = app.property("_translator_gerenciador_traducao")
            if isinstance(trad_instalado, QTranslator):
                app.removeTranslator(trad_instalado)
                app.setProperty("_translator_gerenciador_traducao", None)

            if self.tradutor and self.tradutor is not trad_instalado:
                try:
                    app.removeTranslator(self.tradutor)

                except Exception:
                    pass

            self.tradutor = None

        except Exception as e:
            logger.error(f"Erro ao remover tradutor instalado: {e}", exc_info=True)

    def aplicar_traducao(self):
        try:
            app = self.app or QCoreApplication.instance()

            self._remover_tradutor_instalado()

            if self.idioma_atual == self.idioma_padrao:
                return True

            self.tradutor = QTranslator()
            arquivo_traducao = f"manager_compression_{self.idioma_atual}.qm"
            caminho_traducao = os.path.join(self.dir_traducoes, arquivo_traducao)

            if os.path.exists(caminho_traducao):
                if self.tradutor.load(caminho_traducao):
                    app.installTranslator(self.tradutor)
                    app.setProperty("_translator_gerenciador_traducao", self.tradutor)
                    return True

                else:
                    logger.error(f"Erro ao carregar arquivo de tradução: {caminho_traducao}")

            else:
                logger.warning(f"Arquivo de tradução não encontrado: {caminho_traducao}")
                logger.warning(f"Arquivos disponíveis em {self.dir_traducoes}:")

                try:
                    for arquivo in os.listdir(self.dir_traducoes):
                        logger.warning(f"  - {arquivo}")

                except Exception as e:
                    logger.error(f"Erro ao listar diretório: {e}", exc_info=True)

            return False

        except Exception as e:
            logger.error(f"Erro ao aplicar tradução: {e}", exc_info=True)

    def definir_idioma(self, codigo_idioma):
        try:
            if codigo_idioma in self.idiomas_disponiveis:
                self.idioma_atual = codigo_idioma
                self.salvar_configuracao_idioma()
                resultado = self.aplicar_traducao()
                self.idioma_alterado.emit(codigo_idioma)
                return resultado

            return False

        except Exception as e:
            logger.error(f"Erro ao definir idioma: {e}", exc_info=True)

    def obter_idioma_atual(self):
        try:
            return self.idioma_atual

        except Exception as e:
            logger.error(f"Erro ao obter idioma atual: {e}", exc_info=True)

    def traduzir_botoes_padrao(self, dialogo):
        try:
            botoes = {
                dialogo.Ok: "OK",
                dialogo.Cancel: "Cancelar",
                dialogo.Yes: "Sim",
                dialogo.No: "Não",
                dialogo.Abort: "Abortar",
                dialogo.Retry: "Tentar Novamente",
                dialogo.Ignore: "Ignorar",
                dialogo.Close: "Fechar",
                dialogo.Help: "Ajuda",
                dialogo.Apply: "Aplicar",
                dialogo.Reset: "Redefinir",
                dialogo.RestoreDefaults: "Restaurar Padrões",
                dialogo.Save: "Salvar",
                dialogo.SaveAll: "Salvar Tudo",
                dialogo.Open: "Abrir",
            }

            for botao, texto in botoes.items():
                botao_widget = dialogo.button(botao)
                if botao_widget:
                    botao_widget.setText(QCoreApplication.translate("Dialog", texto))

        except Exception as e:
            logger.error(f"Erro ao traduzir botões padrão: {e}", exc_info=True)
