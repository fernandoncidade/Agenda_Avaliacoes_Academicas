import sys
import signal
import time
from PySide6.QtWidgets import QApplication
from source.GerenciamentoInterfaceGrafica.Interface_Grafica import InterfaceGerenciadorAtividades
from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao
from source.utils.LogManager import LogManager
# from source.utils.TrialManager import TrialManager

logger = LogManager.get_logger()


def iniciar_aplicacao() -> int:
    sinal_sigint_original = signal.getsignal(signal.SIGINT)
    try:
        app = QApplication(sys.argv)

        ultimo_sigint = 0.0

        def tratar_sigint(_sinal, _frame):
            nonlocal ultimo_sigint
            agora = time.monotonic()
            if agora - ultimo_sigint <= 2:
                logger.debug("Aplicação recebeu SIGINT e será encerrada.")
                app.quit()
                return

            ultimo_sigint = agora

        signal.signal(signal.SIGINT, tratar_sigint)

        gerenciador_traducao = GerenciadorTraducao()
        gerenciador_traducao.aplicar_traducao()
        # TrialManager.enforce_trial()  # Descomente esta linha para forçar o uso da versão de avaliação
        # TrialManager.delete_first_run_timestamp()  # Use esta linha para testes, removendo o timestamp de primeiro uso
        window = InterfaceGerenciadorAtividades(gerenciador_traducao)
        window.show()
        exit_code = app.exec()
        logger.debug(f"Aplicação encerrada com código de saída: {exit_code}")
        return int(exit_code)

    except KeyboardInterrupt:
        logger.debug("Aplicação recebeu KeyboardInterrupt e será encerrada.")
        return 0

    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar aplicação: {e}", exc_info=True)
        return 1

    finally:
        signal.signal(signal.SIGINT, sinal_sigint_original)
