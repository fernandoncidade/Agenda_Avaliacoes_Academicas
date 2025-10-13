import os
import sqlite3
import json
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_01_criar_tabela import criar_tabela
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_02_adicionar_atividade import adicionar_atividade
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_03_remover_atividade import remover_atividade
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_04_listar_atividades import listar_atividades
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_05_buscar_atividade import buscar_atividade
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_06_atualizar_atividade import atualizar_atividade
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_07_submiter import submiter
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_08_limpar_entradas import limpar_entradas
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_09_limpar_ultima_entrada import limpar_ultima_entrada
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_10_exportar_para_pdf import exportar_para_pdf
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_11_update_textbox import update_textbox
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_12_excluir_item import excluir_item
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_13_editar_item import editar_item
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_14_editar_detalhes_atividade import editar_detalhes_atividade
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_15_update_ementa import update_ementa
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_16_update_semestre import update_semestre
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_17_update_disciplinas import update_disciplinas
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_18_carregar_dados import carregar_dados
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_19_definir_modo_cores import definir_modo_cores
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_20_obter_modo_cores import obter_modo_cores
from source.GerenciamentoAtividades.GerenciadorAtividades.gativ_21_cor_texto_do_sistema import _cor_texto_do_sistema
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class GerenciamentoAtividades:
    def __init__(self):
        try:
            self.atividades = {}
            self.combo_curso = None
            self.entry_ementa = None
            self.entry_semestre = None
            self.entry_disciplina = None
            self.entry_codigo = None
            self.combo_tipo = None
            self.combo_sequencia = None
            self.calendar = None
            self.textbox = None

            self.modo_cores = "coloridas"

            try:
                persist_dir = obter_caminho_persistente()

            except Exception:
                persist_dir = None

            if not persist_dir:
                persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AgendaAvaliacoesAcademicas")

            os.makedirs(persist_dir, exist_ok=True)

            try:
                config_path = os.path.join(persist_dir, "config.json")
                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        modo = cfg.get("modo_cores")
                        if modo in ("preto", "coloridas"):
                            self.modo_cores = modo

            except Exception:
                pass

            db_path = os.path.join(persist_dir, "atividades.db")

            self.conexao = sqlite3.connect(db_path)
            self.criar_tabela()

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciamentoAtividades: {e}", exc_info=True)

    criar_tabela = criar_tabela
    adicionar_atividade = adicionar_atividade
    remover_atividade = remover_atividade
    listar_atividades = listar_atividades
    buscar_atividade = buscar_atividade
    atualizar_atividade = atualizar_atividade
    submiter = submiter
    limpar_entradas = limpar_entradas
    limpar_ultima_entrada = limpar_ultima_entrada
    exportar_para_pdf = exportar_para_pdf
    update_textbox = update_textbox
    excluir_item = excluir_item
    editar_item = editar_item
    editar_detalhes_atividade = editar_detalhes_atividade
    update_ementa = update_ementa
    update_semestre = update_semestre
    update_disciplinas = update_disciplinas
    carregar_dados = carregar_dados
    definir_modo_cores = definir_modo_cores
    obter_modo_cores = obter_modo_cores
    cor_texto_do_sistema = _cor_texto_do_sistema
