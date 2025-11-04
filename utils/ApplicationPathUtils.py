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

def get_text_file_path(filename, folder=None):
    try:
        base_path = get_app_base_path()
        possible_paths = []
        if folder:
            possible_paths = [
                os.path.join(base_path, "assets", folder, filename),
                os.path.join(base_path, folder, filename),
                os.path.join(base_path, "_internal", "assets", folder, filename),
                os.path.join(base_path, "_internal", folder, filename),
                os.path.join(os.path.dirname(base_path), "assets", folder, filename),
                os.path.join(os.path.dirname(base_path), folder, filename),
                os.path.join(base_path, "main.dist", "assets", folder, filename),
                os.path.join(base_path, "dist", "main.dist", "assets", folder, filename)
            ]

        else:
            possible_paths = [
                os.path.join(base_path, "assets", filename),
                os.path.join(base_path, filename),
                os.path.join(base_path, "_internal", "assets", filename),
                os.path.join(base_path, "_internal", filename),
                os.path.join(os.path.dirname(base_path), "assets", filename),
                os.path.join(os.path.dirname(base_path), filename),
                os.path.join(base_path, "main.dist", "assets", filename),
                os.path.join(base_path, "dist", "main.dist", "assets", filename)
            ]

        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path

        return os.path.abspath(possible_paths[0])

    except Exception as e:
        logger.error(f"Erro ao obter caminho do arquivo de texto '{filename}': {e}")
        return None

def load_text_file(filename, folder=None, encoding="utf-8"):
    try:
        file_path = get_text_file_path(filename, folder)
        if file_path:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()

        else:
            logger.error(f"Arquivo de texto '{filename}' não encontrado.")
            return None

    except Exception as e:
        logger.error(f"Erro ao carregar arquivo de texto '{filename}': {e}")
        return None
