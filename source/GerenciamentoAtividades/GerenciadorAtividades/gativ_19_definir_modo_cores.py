import os
import json
from utils.LogManager import LogManager
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
logger = LogManager.get_logger()

def definir_modo_cores(self, modo):
    try:
        if modo not in ("preto", "coloridas"):
            return False

        self.modo_cores = modo

        try:
            persist_dir = os.path.dirname(self.conexao.execute("PRAGMA database_list").fetchall()[0][2]) if hasattr(self, 'conexao') else None

        except Exception:
            persist_dir = None

        if not persist_dir:
            try:
                persist_dir = obter_caminho_persistente()

            except Exception:
                persist_dir = None

        if not persist_dir:
            persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AgendaAvaliacoesAcademicas")

        os.makedirs(persist_dir, exist_ok=True)
        config_path = os.path.join(persist_dir, "config.json")

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"modo_cores": self.modo_cores}, f, ensure_ascii=False, indent=2)

        except Exception:
            pass

        return True

    except Exception as e:
        logger.error(f"Erro ao definir modo de cores: {e}", exc_info=True)
        return False
