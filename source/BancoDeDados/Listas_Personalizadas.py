import os
import sqlite3
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

_tabelas_criadas = False

_CATEGORIAS_EXCLUSAO = {
    "curso": {
        "tabela": "lista_cursos",
        "select": "SELECT id, valor FROM lista_cursos WHERE idioma = ? ORDER BY valor COLLATE NOCASE",
    },
    "ementa": {
        "tabela": "lista_ementas",
        "select": """
            SELECT id, curso, valor FROM lista_ementas
            WHERE idioma = ?
            ORDER BY curso COLLATE NOCASE, valor COLLATE NOCASE
        """,
    },
    "semestre": {
        "tabela": "lista_semestres",
        "select": """
            SELECT id, curso, ementa, valor FROM lista_semestres
            WHERE idioma = ?
            ORDER BY curso COLLATE NOCASE, ementa COLLATE NOCASE, valor COLLATE NOCASE
        """,
    },
    "disciplina": {
        "tabela": "lista_disciplinas",
        "select": """
            SELECT id, curso, ementa, semestre, valor FROM lista_disciplinas
            WHERE idioma = ?
            ORDER BY curso COLLATE NOCASE, ementa COLLATE NOCASE, semestre COLLATE NOCASE, valor COLLATE NOCASE
        """,
    },
    "turma": {
        "tabela": "lista_turmas",
        "select": "SELECT id, valor FROM lista_turmas WHERE idioma = ? ORDER BY valor COLLATE NOCASE",
    },
    "tipo": {
        "tabela": "lista_tipos_atividade",
        "select": "SELECT id, valor FROM lista_tipos_atividade WHERE idioma = ? ORDER BY valor COLLATE NOCASE",
    },
    "sequencia": {
        "tabela": "lista_sequencias_atividade",
        "select": "SELECT id, valor FROM lista_sequencias_atividade WHERE idioma = ? ORDER BY valor COLLATE NOCASE",
    },
}


def _texto(valor):
    if valor is None:
        return ""

    return str(valor).strip()


def _normalizar(valor):
    return _texto(valor).casefold()


def obter_caminho_listas_db():
    persist_dir = obter_caminho_persistente()
    os.makedirs(persist_dir, exist_ok=True)
    return os.path.join(persist_dir, "listas.db")


def _abrir_conexao():
    return sqlite3.connect(obter_caminho_listas_db())


def criar_tabelas_listas():
    global _tabelas_criadas
    if _tabelas_criadas:
        return

    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_ementas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                curso TEXT NOT NULL,
                curso_normalizado TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, curso_normalizado, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_semestres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                curso TEXT NOT NULL,
                curso_normalizado TEXT NOT NULL,
                ementa TEXT NOT NULL,
                ementa_normalizada TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, curso_normalizado, ementa_normalizada, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                curso TEXT NOT NULL,
                curso_normalizado TEXT NOT NULL,
                ementa TEXT NOT NULL,
                ementa_normalizada TEXT NOT NULL,
                semestre TEXT NOT NULL,
                semestre_normalizado TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, curso_normalizado, ementa_normalizada, semestre_normalizado, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_tipos_atividade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, valor_normalizado)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lista_sequencias_atividade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                valor TEXT NOT NULL,
                valor_normalizado TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(idioma, valor_normalizado)
            )
        """)
        conexao.commit()
        _tabelas_criadas = True

    except Exception as e:
        logger.error(f"Erro ao criar tabelas de listas personalizadas: {e}", exc_info=True)

    finally:
        if conexao is not None:
            conexao.close()


def _listar_simples(tabela, idioma):
    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            f"SELECT valor FROM {tabela} WHERE idioma = ? ORDER BY valor COLLATE NOCASE",
            (_texto(idioma),),
        )
        return [linha[0] for linha in cursor.fetchall()]

    except Exception as e:
        logger.error(f"Erro ao listar valores personalizados de {tabela}: {e}", exc_info=True)
        return []

    finally:
        if conexao is not None:
            conexao.close()


def _inserir_simples(tabela, idioma, valor):
    valor = _texto(valor)
    if not valor:
        return False

    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {tabela} (idioma, valor, valor_normalizado)
            VALUES (?, ?, ?)
            """,
            (_texto(idioma), valor, _normalizar(valor)),
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao inserir valor personalizado em {tabela}: {e}", exc_info=True)
        return False

    finally:
        if conexao is not None:
            conexao.close()


def listar_cursos(idioma):
    return _listar_simples("lista_cursos", idioma)


def listar_turmas(idioma):
    return _listar_simples("lista_turmas", idioma)


def listar_tipos_atividade(idioma):
    return _listar_simples("lista_tipos_atividade", idioma)


def listar_sequencias_atividade(idioma):
    return _listar_simples("lista_sequencias_atividade", idioma)


def inserir_curso(idioma, curso):
    return _inserir_simples("lista_cursos", idioma, curso)


def inserir_turma(idioma, turma):
    return _inserir_simples("lista_turmas", idioma, turma)


def inserir_tipo_atividade(idioma, tipo):
    return _inserir_simples("lista_tipos_atividade", idioma, tipo)


def inserir_sequencia_atividade(idioma, sequencia):
    return _inserir_simples("lista_sequencias_atividade", idioma, sequencia)


def listar_ementas(idioma, curso):
    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT valor FROM lista_ementas
            WHERE idioma = ? AND curso_normalizado = ?
            ORDER BY valor COLLATE NOCASE
            """,
            (_texto(idioma), _normalizar(curso)),
        )
        return [linha[0] for linha in cursor.fetchall()]

    except Exception as e:
        logger.error(f"Erro ao listar ementas personalizadas: {e}", exc_info=True)
        return []

    finally:
        if conexao is not None:
            conexao.close()


def listar_semestres(idioma, curso, ementa):
    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT valor FROM lista_semestres
            WHERE idioma = ? AND curso_normalizado = ? AND ementa_normalizada = ?
            ORDER BY valor COLLATE NOCASE
            """,
            (_texto(idioma), _normalizar(curso), _normalizar(ementa)),
        )
        return [linha[0] for linha in cursor.fetchall()]

    except Exception as e:
        logger.error(f"Erro ao listar semestres personalizados: {e}", exc_info=True)
        return []

    finally:
        if conexao is not None:
            conexao.close()


def listar_disciplinas(idioma, curso, ementa, semestre):
    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT valor FROM lista_disciplinas
            WHERE idioma = ?
              AND curso_normalizado = ?
              AND ementa_normalizada = ?
              AND semestre_normalizado = ?
            ORDER BY valor COLLATE NOCASE
            """,
            (_texto(idioma), _normalizar(curso), _normalizar(ementa), _normalizar(semestre)),
        )
        return [linha[0] for linha in cursor.fetchall()]

    except Exception as e:
        logger.error(f"Erro ao listar disciplinas personalizadas: {e}", exc_info=True)
        return []

    finally:
        if conexao is not None:
            conexao.close()


def inserir_ementa(idioma, curso, ementa):
    curso = _texto(curso)
    ementa = _texto(ementa)
    if not curso or not ementa:
        return False

    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO lista_ementas (
                idioma, curso, curso_normalizado, valor, valor_normalizado
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (_texto(idioma), curso, _normalizar(curso), ementa, _normalizar(ementa)),
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao inserir ementa personalizada: {e}", exc_info=True)
        return False

    finally:
        if conexao is not None:
            conexao.close()


def inserir_semestre(idioma, curso, ementa, semestre):
    curso = _texto(curso)
    ementa = _texto(ementa)
    semestre = _texto(semestre)
    if not curso or not ementa or not semestre:
        return False

    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO lista_semestres (
                idioma, curso, curso_normalizado, ementa, ementa_normalizada, valor, valor_normalizado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _texto(idioma),
                curso,
                _normalizar(curso),
                ementa,
                _normalizar(ementa),
                semestre,
                _normalizar(semestre),
            ),
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao inserir semestre personalizado: {e}", exc_info=True)
        return False

    finally:
        if conexao is not None:
            conexao.close()


def inserir_disciplina(idioma, curso, ementa, semestre, disciplina):
    curso = _texto(curso)
    ementa = _texto(ementa)
    semestre = _texto(semestre)
    disciplina = _texto(disciplina)
    if not curso or not ementa or not semestre or not disciplina:
        return False

    criar_tabelas_listas()
    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO lista_disciplinas (
                idioma,
                curso,
                curso_normalizado,
                ementa,
                ementa_normalizada,
                semestre,
                semestre_normalizado,
                valor,
                valor_normalizado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _texto(idioma),
                curso,
                _normalizar(curso),
                ementa,
                _normalizar(ementa),
                semestre,
                _normalizar(semestre),
                disciplina,
                _normalizar(disciplina),
            ),
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao inserir disciplina personalizada: {e}", exc_info=True)
        return False

    finally:
        if conexao is not None:
            conexao.close()


def registrar_listas_personalizadas(
    idioma,
    curso="",
    ementa="",
    semestre="",
    disciplina="",
    turma="",
    tipo="",
    sequencia="",
):
    resultados = {
        "curso": inserir_curso(idioma, curso),
        "ementa": inserir_ementa(idioma, curso, ementa),
        "semestre": inserir_semestre(idioma, curso, ementa, semestre),
        "disciplina": inserir_disciplina(idioma, curso, ementa, semestre, disciplina),
        "turma": inserir_turma(idioma, turma),
        "tipo": inserir_tipo_atividade(idioma, tipo),
        "sequencia": inserir_sequencia_atividade(idioma, sequencia),
    }
    return resultados


def _formatar_item_personalizado(categoria, linha):
    if categoria in ("curso", "turma", "tipo", "sequencia"):
        return linha[1]

    if categoria == "ementa":
        return f"{linha[1]} > {linha[2]}"

    if categoria == "semestre":
        return f"{linha[1]} > {linha[2]} > {linha[3]}"

    if categoria == "disciplina":
        return f"{linha[1]} > {linha[2]} > {linha[3]} > {linha[4]}"

    return ""


def listar_itens_personalizados_para_exclusao(categoria, idioma):
    criar_tabelas_listas()
    config = _CATEGORIAS_EXCLUSAO.get(categoria)
    if not config:
        return []

    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(config["select"], (_texto(idioma),))
        return [
            {
                "id": linha[0],
                "categoria": categoria,
                "texto": _formatar_item_personalizado(categoria, linha),
            }
            for linha in cursor.fetchall()
        ]

    except Exception as e:
        logger.error(f"Erro ao listar itens personalizados para exclusão: {e}", exc_info=True)
        return []

    finally:
        if conexao is not None:
            conexao.close()


def remover_item_personalizado(categoria, item_id):
    criar_tabelas_listas()
    config = _CATEGORIAS_EXCLUSAO.get(categoria)
    if not config:
        return False

    conexao = None
    try:
        conexao = _abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute(f"DELETE FROM {config['tabela']} WHERE id = ?", (int(item_id),))
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao remover item personalizado: {e}", exc_info=True)
        return False

    finally:
        if conexao is not None:
            conexao.close()
