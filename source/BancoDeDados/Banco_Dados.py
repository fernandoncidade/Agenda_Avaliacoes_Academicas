import re
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

try:
    from .DicionariosListasBancoDeDados.lista_cursos_pt_BR import lista_cursos_pt_BR
    from .DicionariosListasBancoDeDados.lista_cursos_en_US import lista_cursos_en_US
    from .DicionariosListasBancoDeDados.lista_turmas_pt_BR import lista_turmas_pt_BR
    from .DicionariosListasBancoDeDados.lista_turmas_en_US import lista_turmas_en_US
    from .DicionariosListasBancoDeDados.lista_avaliacoes_pt_BR import lista_avaliacoes_pt_BR
    from .DicionariosListasBancoDeDados.lista_avaliacoes_en_US import lista_avaliacoes_en_US
    from .DicionariosListasBancoDeDados.mapeamento_cursos import mapeamento_cursos
    from .DicionariosListasBancoDeDados.mapeamento_ementas import mapeamento_ementas
    from .DicionariosListasBancoDeDados.mapeamento_semestres import mapeamento_semestres
    from .DicionariosListasBancoDeDados.CURSOS_PT import CURSOS_PT
    from .DicionariosListasBancoDeDados.CURSOS_EN import CURSOS_EN
    from .DicionariosListasBancoDeDados.dicionario_disciplinas import dicionario_disciplinas
    from .DicionariosListasBancoDeDados.dicionario_de_cores import dicionario_de_cores

except Exception:
    try:
        from DicionariosListasBancoDeDados.lista_cursos_pt_BR import lista_cursos_pt_BR
        from DicionariosListasBancoDeDados.lista_cursos_en_US import lista_cursos_en_US
        from DicionariosListasBancoDeDados.lista_turmas_pt_BR import lista_turmas_pt_BR
        from DicionariosListasBancoDeDados.lista_turmas_en_US import lista_turmas_en_US
        from DicionariosListasBancoDeDados.lista_avaliacoes_pt_BR import lista_avaliacoes_pt_BR
        from DicionariosListasBancoDeDados.lista_avaliacoes_en_US import lista_avaliacoes_en_US
        from DicionariosListasBancoDeDados.mapeamento_cursos import mapeamento_cursos
        from DicionariosListasBancoDeDados.mapeamento_ementas import mapeamento_ementas
        from DicionariosListasBancoDeDados.mapeamento_semestres import mapeamento_semestres
        from DicionariosListasBancoDeDados.CURSOS_PT import CURSOS_PT
        from DicionariosListasBancoDeDados.CURSOS_EN import CURSOS_EN
        from DicionariosListasBancoDeDados.dicionario_disciplinas import dicionario_disciplinas
        from DicionariosListasBancoDeDados.dicionario_de_cores import dicionario_de_cores

    except Exception:
        lista_cursos_pt_BR = []
        lista_cursos_en_US = []
        lista_turmas_pt_BR = []
        lista_turmas_en_US = []
        lista_avaliacoes_pt_BR = []
        lista_avaliacoes_en_US = []
        mapeamento_cursos = {}
        mapeamento_ementas = {}
        mapeamento_semestres = {}
        CURSOS_PT = {}
        CURSOS_EN = {}
        dicionario_disciplinas = {}
        dicionario_de_cores = {}

def obter_idioma_atual():
    try:
        from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao
        gerenciador = GerenciadorTraducao()
        return gerenciador.obter_idioma_atual()

    except Exception:
        return "pt_BR"

def _mesclar_listas(*listas):
    resultado = []
    vistos = set()
    for lista in listas:
        for item in lista or []:
            texto = "" if item is None else str(item)
            chave = texto.strip().casefold()
            if chave in vistos:
                continue

            vistos.add(chave)
            resultado.append(texto)

    return resultado

def obter_cursos():
    try:
        idioma = obter_idioma_atual()
        base = lista_cursos_en_US if idioma == "en_US" else lista_cursos_pt_BR
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_cursos
            return _mesclar_listas(base, listar_cursos(idioma))

        except Exception as e:
            logger.error(f"Erro ao obter cursos personalizados: {e}", exc_info=True)

        if idioma == "en_US":
            return lista_cursos_en_US

        return lista_cursos_pt_BR
    
    except Exception as e:
        logger.error(f"Erro ao obter cursos: {e}", exc_info=True)

def obter_turmas():
    try:
        idioma = obter_idioma_atual()
        base = lista_turmas_en_US if idioma == "en_US" else lista_turmas_pt_BR
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_turmas
            return _mesclar_listas(base, listar_turmas(idioma))

        except Exception as e:
            logger.error(f"Erro ao obter turmas personalizadas: {e}", exc_info=True)

        if idioma == "en_US":
            return lista_turmas_en_US

        return lista_turmas_pt_BR

    except Exception as e:
        logger.error(f"Erro ao obter turmas: {e}", exc_info=True)

    return lista_turmas_pt_BR

def obter_avaliacoes():
    try:
        idioma = obter_idioma_atual()
        base = lista_avaliacoes_en_US if idioma == "en_US" else lista_avaliacoes_pt_BR
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_tipos_atividade
            return _mesclar_listas(base, listar_tipos_atividade(idioma))

        except Exception as e:
            logger.error(f"Erro ao obter tipos de atividade personalizados: {e}", exc_info=True)

        if idioma == "en_US":
            return lista_avaliacoes_en_US

        return lista_avaliacoes_pt_BR

    except Exception as e:
        logger.error(f"Erro ao obter avaliações: {e}", exc_info=True)

def obter_sequencias():
    try:
        idioma = obter_idioma_atual()
        base = [""] + [str(i) for i in range(1, 11)]
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_sequencias_atividade
            return _mesclar_listas(base, listar_sequencias_atividade(idioma))

        except Exception as e:
            logger.error(f"Erro ao obter sequências personalizadas: {e}", exc_info=True)

        return base

    except Exception as e:
        logger.error(f"Erro ao obter sequências: {e}", exc_info=True)
        return [""] + [str(i) for i in range(1, 11)]

def traduzir_curso(curso, idioma_destino=None):
    try:
        if idioma_destino is None:
            idioma_destino = obter_idioma_atual()

        if idioma_destino == "pt_BR":
            return curso

        return mapeamento_cursos.get(idioma_destino, {}).get(curso, curso)

    except Exception as e:
        logger.error(f"Erro ao traduzir curso '{curso}': {e}", exc_info=True)

def traduzir_ementa(ementa, idioma_destino=None):
    try:
        if idioma_destino is None:
            idioma_destino = obter_idioma_atual()

        if idioma_destino == "pt_BR":
            return ementa

        return mapeamento_ementas.get(idioma_destino, {}).get(ementa, ementa)

    except Exception as e:
        logger.error(f"Erro ao traduzir ementa '{ementa}': {e}", exc_info=True)

def traduzir_semestre(semestre, idioma_destino=None):
    try:
        if idioma_destino is None:
            idioma_destino = obter_idioma_atual()

        if idioma_destino == "pt_BR":
            return semestre

        return mapeamento_semestres.get(idioma_destino, {}).get(semestre, semestre)

    except Exception as e:
        logger.error(f"Erro ao traduzir semestre '{semestre}': {e}", exc_info=True)

def obter_estrutura_cursos():
    try:
        idioma = obter_idioma_atual()
        if idioma == "en_US":
            return CURSOS_EN

        return CURSOS_PT

    except Exception as e:
        logger.error(f"Erro ao obter estrutura de cursos: {e}", exc_info=True)

def obter_ementas(curso):
    try:
        idioma = obter_idioma_atual()
        estrutura = obter_estrutura_cursos()
        ementas_personalizadas = []
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_ementas
            ementas_personalizadas = listar_ementas(idioma, curso)

        except Exception as e:
            logger.error(f"Erro ao obter ementas personalizadas para o curso '{curso}': {e}", exc_info=True)

        if not curso:
            return _mesclar_listas(ementas_personalizadas)

        if curso in estrutura:
            return _mesclar_listas(list(estrutura.get(curso, {}).keys()), ementas_personalizadas)

        for chave in estrutura.keys():
            if chave.lower() == curso.lower():
                return _mesclar_listas(list(estrutura.get(chave, {}).keys()), ementas_personalizadas)

        return _mesclar_listas(ementas_personalizadas)

    except Exception as e:
        logger.error(f"Erro ao obter ementas para o curso '{curso}': {e}", exc_info=True)
        return []

def obter_semestres(curso, ementa):
    try:
        idioma = obter_idioma_atual()
        estrutura = obter_estrutura_cursos()
        semestres_personalizados = []
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_semestres
            semestres_personalizados = listar_semestres(idioma, curso, ementa)

        except Exception as e:
            logger.error(f"Erro ao obter semestres personalizados para o curso '{curso}': {e}", exc_info=True)

        if not curso or not ementa:
            return _mesclar_listas(semestres_personalizados)

        cursos_keys = estrutura.get(curso)
        if cursos_keys and ementa in cursos_keys:
            base = list(cursos_keys[ementa].keys()) if isinstance(cursos_keys[ementa], dict) else []
            return _mesclar_listas(base, semestres_personalizados)

        for ck, v in estrutura.items():
            if ck.lower() == curso.lower():
                for em in v.keys():
                    if em.lower() == ementa.lower():
                        base = list(v[em].keys()) if isinstance(v[em], dict) else []
                        return _mesclar_listas(base, semestres_personalizados)

        return _mesclar_listas(semestres_personalizados)

    except Exception as e:
        logger.error(f"Erro ao obter ementas para o curso '{curso}': {e}", exc_info=True)
        return []

def obter_disciplinas(curso, ementa, semestre):
    try:
        idioma = obter_idioma_atual()
        estrutura = obter_estrutura_cursos()
        disciplinas_personalizadas = []
        try:
            from source.BancoDeDados.Listas_Personalizadas import listar_disciplinas
            disciplinas_personalizadas = listar_disciplinas(idioma, curso, ementa, semestre)

        except Exception as e:
            logger.error(f"Erro ao obter disciplinas personalizadas para o curso '{curso}': {e}", exc_info=True)

        if not curso or not ementa or not semestre:
            return _mesclar_listas(disciplinas_personalizadas)

        cursos_keys = estrutura.get(curso)
        if cursos_keys:
            ementa_obj = cursos_keys.get(ementa)
            if isinstance(ementa_obj, dict) and semestre in ementa_obj:
                return _mesclar_listas(list(ementa_obj[semestre]), disciplinas_personalizadas)

            for em, sems in cursos_keys.items():
                if em.lower() == ementa.lower():
                    if isinstance(sems, dict):
                        for s_key, disciplinas in sems.items():
                            if s_key.lower() == semestre.lower():
                                return _mesclar_listas(list(disciplinas), disciplinas_personalizadas)

        for ck, cval in estrutura.items():
            for em, sems in cval.items():
                if em.lower() == ementa.lower():
                    for s_key, disciplinas in sems.items():
                        if s_key.lower() == semestre.lower():
                            return _mesclar_listas(list(disciplinas), disciplinas_personalizadas)

        return _mesclar_listas(disciplinas_personalizadas)

    except Exception as e:
        logger.error(f"Erro ao obter disciplinas para o curso '{curso}', ementa '{ementa}' e semestre '{semestre}': {e}", exc_info=True)
        return []

def registrar_valores_personalizados(
    curso="",
    ementa="",
    semestre="",
    disciplina="",
    turma="",
    tipo="",
    sequencia="",
    registrar_curso=False,
    registrar_ementa=False,
    registrar_semestre=False,
    registrar_disciplina=False,
    registrar_turma=False,
    registrar_tipo=False,
    registrar_sequencia=False,
):
    try:
        from source.BancoDeDados import Listas_Personalizadas as listas_personalizadas

        idioma = obter_idioma_atual()
        resultados = {}
        if registrar_curso:
            resultados["curso"] = listas_personalizadas.inserir_curso(idioma, curso)

        if registrar_ementa:
            resultados["ementa"] = listas_personalizadas.inserir_ementa(idioma, curso, ementa)

        if registrar_semestre:
            resultados["semestre"] = listas_personalizadas.inserir_semestre(idioma, curso, ementa, semestre)

        if registrar_disciplina:
            resultados["disciplina"] = listas_personalizadas.inserir_disciplina(idioma, curso, ementa, semestre, disciplina)

        if registrar_turma:
            resultados["turma"] = listas_personalizadas.inserir_turma(idioma, turma)

        if registrar_tipo:
            resultados["tipo"] = listas_personalizadas.inserir_tipo_atividade(idioma, tipo)

        if registrar_sequencia:
            resultados["sequencia"] = listas_personalizadas.inserir_sequencia_atividade(idioma, sequencia)

        return resultados

    except Exception as e:
        logger.error(f"Erro ao registrar valores personalizados: {e}", exc_info=True)
        return {}

def atualizar_listas_exportadas():
    try:
        global lista_cursos, lista_turmas, lista_avaliacoes, lista_sequencias
        lista_cursos = obter_cursos()
        lista_turmas = obter_turmas()
        lista_avaliacoes = obter_avaliacoes()
        lista_sequencias = obter_sequencias()

    except Exception as e:
        logger.error(f"Erro ao atualizar listas exportadas: {e}", exc_info=True)

lista_cursos = obter_cursos()
lista_turmas = obter_turmas()
lista_avaliacoes = obter_avaliacoes()
lista_sequencias = obter_sequencias()

def construir_mapeamento_codigo_para_cor():
    try:
        mapping = {}
        pattern = re.compile(r'([A-Z]{1,3}\d{3,4})$')
        for coloracao, disciplinas in dicionario_disciplinas.items():
            cor = dicionario_de_cores.get(coloracao)
            for d in disciplinas:
                if not d:
                    continue

                m = pattern.search(d.strip())
                if m and cor:
                    mapping[m.group(1)] = cor

        return mapping

    except Exception as e:
        logger.error(f"Erro ao construir mapeamento de código para cor: {e}", exc_info=True)

mapeamento_codigo_cor = construir_mapeamento_codigo_para_cor()

def obter_cor_por_nome(nome_disciplina):
    try:
        if not nome_disciplina:
            return None

        nome = nome_disciplina.strip()

        m = re.search(r'([A-Z]{1,3}\d{3,4})$', nome)
        if m:
            codigo = m.group(1)
            cor = mapeamento_codigo_cor.get(codigo)
            if cor:
                return cor

        lower = nome.lower()
        for coloracao, disciplinas in dicionario_disciplinas.items():
            for d in disciplinas:
                if d and d.lower() == lower:
                    return dicionario_de_cores.get(coloracao)

        return None

    except Exception as e:
        logger.error(f"Erro ao obter cor por nome '{nome_disciplina}': {e}", exc_info=True)
        return None
