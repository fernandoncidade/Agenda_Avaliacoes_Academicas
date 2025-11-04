from utils.LogManager import LogManager

logger = LogManager.get_logger()

def change_color_mode(self, codigo_modo):
    try:
        if not hasattr(self, 'gerenciamento_atividades'):
            return

        success = False
        try:
            success = self.gerenciamento_atividades.definir_modo_cores(codigo_modo)

        except Exception:
            success = False

        if success:
            self.update_textbox()
            for c, a in self.color_actions.items():
                a.setChecked(c == codigo_modo)

        else:
            atual = self.gerenciamento_atividades.obter_modo_cores()
            if atual in self.color_actions:
                self.color_actions[atual].setChecked(True)

    except Exception as e:
        logger.critical(f"Erro fatal ao mudar modo de cores: {e}", exc_info=True)
