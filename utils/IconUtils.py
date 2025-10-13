import os
import sys
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_app_base_path():
    try:
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS

            else:
                exe_dir = os.path.dirname(sys.executable)
                if "WindowsApps" in exe_dir:
                    return exe_dir

                return exe_dir

        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    except Exception as e:
        logger.error(f"Erro ao obter caminho base do app: {e}")
        return None

def get_icon_path(icon_name):
    try:
        base_path = get_app_base_path()
        possible_paths = [
            os.path.join(base_path, "assets", "icones", icon_name),
            os.path.join(base_path, "icones", icon_name),
            os.path.join(base_path, "_internal", "icones", icon_name),
            os.path.join(os.path.dirname(__file__), "..", "assets", "icones", icon_name),
            os.path.join(os.path.dirname(__file__), "..", "icones", icon_name)
        ]
        for icon_path in possible_paths:
            icon_path = os.path.abspath(icon_path)
            if os.path.exists(icon_path):
                return icon_path

        return os.path.abspath(possible_paths[0])

    except Exception as e:
        logger.error(f"Erro ao obter caminho do ícone '{icon_name}': {e}")
        return None
