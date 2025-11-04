from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QLabel, QComboBox, QCalendarWidget, QTextBrowser, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from source.BancoDeDados.Banco_Dados import lista_cursos, lista_turmas, lista_avaliacoes
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_widgets(self):
    try:
        layout_horizontal_1 = QHBoxLayout()
        layout_vertical_1 = QVBoxLayout()

        self.label_curso = QLabel()
        self.combo_curso = QComboBox()
        self.combo_curso.setMinimumWidth(300)
        self.combo_curso.setMaximumWidth(300)
        self.combo_curso.addItems(lista_cursos)
        self.combo_curso.currentTextChanged.connect(self.update_ementa)
        layout_vertical_1.addWidget(self.label_curso)
        layout_vertical_1.addWidget(self.combo_curso)

        self.label_ementa = QLabel()
        self.entry_ementa = QComboBox()
        self.entry_ementa.setMinimumWidth(300)
        self.entry_ementa.setMaximumWidth(300)
        self.entry_ementa.currentTextChanged.connect(self.update_semestre)
        layout_vertical_1.addWidget(self.label_ementa)
        layout_vertical_1.addWidget(self.entry_ementa)

        self.label_semestre = QLabel()
        self.entry_semestre = QComboBox()
        self.entry_semestre.setMinimumWidth(300)
        self.entry_semestre.setMaximumWidth(300)
        self.entry_semestre.currentTextChanged.connect(self.update_disciplinas)
        layout_vertical_1.addWidget(self.label_semestre)
        layout_vertical_1.addWidget(self.entry_semestre)

        self.label_disciplina = QLabel()
        self.entry_disciplina = QComboBox()
        self.entry_disciplina.setMinimumWidth(300)
        self.entry_disciplina.setMaximumWidth(300)
        layout_vertical_1.addWidget(self.label_disciplina)
        layout_vertical_1.addWidget(self.entry_disciplina)

        self.label_codigo = QLabel()
        self.entry_codigo = QComboBox()
        self.entry_codigo.setMinimumWidth(300)
        self.entry_codigo.setMaximumWidth(300)
        self.entry_codigo.addItems(lista_turmas)
        layout_vertical_1.addWidget(self.label_codigo)
        layout_vertical_1.addWidget(self.entry_codigo)

        self.label_tipo = QLabel()
        self.combo_tipo = QComboBox()
        self.combo_tipo.setMinimumWidth(300)
        self.combo_tipo.setMaximumWidth(300)
        self.combo_tipo.addItems(lista_avaliacoes)
        layout_vertical_1.addWidget(self.label_tipo)
        layout_vertical_1.addWidget(self.combo_tipo)

        self.label_sequencia = QLabel()
        self.combo_sequencia = QComboBox()
        self.combo_sequencia.setMinimumWidth(300)
        self.combo_sequencia.setMaximumWidth(300)
        self.combo_sequencia.addItems([""] + [str(i) for i in range(1, 11)])
        layout_vertical_1.addWidget(self.label_sequencia)
        layout_vertical_1.addWidget(self.combo_sequencia)

        self.label_data = QLabel()
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumWidth(300)
        self.calendar.setMaximumWidth(300)
        self.calendar.setMaximumHeight(200)
        layout_vertical_1.addWidget(self.label_data)
        layout_vertical_1.addWidget(self.calendar)

        layout_botaoes = QHBoxLayout()
        layout_sub_vertical_1 = QVBoxLayout()
        layout_sub_vertical_2 = QVBoxLayout()

        self.button_clear_item = self.create_button()
        self.button_clear_item.clicked.connect(self.excluir_item)
        self.button_clear_ultima = self.create_button()
        self.button_clear_ultima.clicked.connect(self.limpar_ultima_entrada)
        self.button_clear = self.create_button()
        self.button_clear.clicked.connect(self.limpar_entradas)
        self.button_editar_item = self.create_button()
        self.button_editar_item.clicked.connect(self.editar_item)
        self.button_submiter = self.create_button()
        self.button_submiter.clicked.connect(self.submiter)
        self.button_export = self.create_button()
        self.button_export.clicked.connect(self.exportar_para_pdf)

        layout_sub_vertical_1.addWidget(self.button_clear_item)
        layout_sub_vertical_1.addWidget(self.button_clear_ultima)
        layout_sub_vertical_1.addWidget(self.button_clear)
        layout_sub_vertical_2.addWidget(self.button_editar_item)
        layout_sub_vertical_2.addWidget(self.button_submiter)
        layout_sub_vertical_2.addWidget(self.button_export)
        layout_sub_vertical_1.setAlignment(self.button_clear_item, Qt.AlignLeft)
        layout_sub_vertical_1.setAlignment(self.button_clear_ultima, Qt.AlignLeft)
        layout_sub_vertical_1.setAlignment(self.button_clear, Qt.AlignLeft)
        layout_sub_vertical_2.setAlignment(self.button_editar_item, Qt.AlignRight)
        layout_sub_vertical_2.setAlignment(self.button_submiter, Qt.AlignRight)
        layout_sub_vertical_2.setAlignment(self.button_export, Qt.AlignRight)

        layout_botaoes.addLayout(layout_sub_vertical_1)
        layout_botaoes.addLayout(layout_sub_vertical_2)
        layout_vertical_1.addLayout(layout_botaoes)
        layout_vertical_1.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout_horizontal_1.addLayout(layout_vertical_1)

        layout_vertical_2 = QVBoxLayout()

        self.label_banco_dados = QLabel()
        self.textbox = QTextBrowser()
        self.textbox.setMinimumWidth(600)
        layout_vertical_2.addWidget(self.label_banco_dados)
        layout_vertical_2.addWidget(self.textbox)
        layout_horizontal_1.addLayout(layout_vertical_2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_horizontal_1)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.gerenciamento_atividades.textbox = self.textbox
        self.gerenciamento_atividades.combo_curso = self.combo_curso
        self.gerenciamento_atividades.entry_codigo = self.entry_codigo
        self.gerenciamento_atividades.combo_tipo = self.combo_tipo
        self.gerenciamento_atividades.combo_sequencia = self.combo_sequencia
        self.gerenciamento_atividades.calendar = self.calendar
        self.gerenciamento_atividades.entry_disciplina = self.entry_disciplina
        self.gerenciamento_atividades.entry_ementa = self.entry_ementa
        self.gerenciamento_atividades.entry_semestre = self.entry_semestre

    except Exception as e:
        logger.critical(f"Erro fatal ao criar widgets: {e}", exc_info=True)
