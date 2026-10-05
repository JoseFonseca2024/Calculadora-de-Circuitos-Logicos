from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
    QRadioButton,
    QButtonGroup,
    QGridLayout,
    QFrame
)


class InputWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.variable_edits = []

        # ==========================================================
        # LAYOUT PRINCIPAL
        # ==========================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        layout.setSpacing(12)

        # ==========================================================
        # CONFIGURACIÓN DE ENTRADAS
        # ==========================================================

        config_box = QGroupBox(
            "Configuración de entradas"
        )

        config_box.setObjectName(
            "card_panel"
        )

        config_layout = QVBoxLayout(
            config_box
        )

        config_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        config_layout.setSpacing(10)

        # ----------------------------------------------------------
        # Número de entradas
        # ----------------------------------------------------------

        number_row = QHBoxLayout()

        number_label = QLabel(
            "Número de entradas:"
        )

        number_row.addWidget(
            number_label
        )

        self.number_inputs = QSpinBox()

        self.number_inputs.setMinimum(2)
        self.number_inputs.setMaximum(6)
        self.number_inputs.setValue(4)

        self.number_inputs.setFixedWidth(
            80
        )

        number_row.addWidget(
            self.number_inputs
        )

        number_row.addStretch()

        config_layout.addLayout(
            number_row
        )

        # ----------------------------------------------------------
        # Nombre de entradas
        # ----------------------------------------------------------

        name_label = QLabel(
            "Nombre de las entradas:"
        )

        name_label.setObjectName(
            "section_label"
        )

        config_layout.addWidget(
            name_label
        )

        # ----------------------------------------------------------
        # Radio buttons
        # ----------------------------------------------------------

        radio_row = QHBoxLayout()

        radio_row.setSpacing(20)

        self.radio_abc = QRadioButton(
            "A, B, C, D..."
        )

        self.radio_x = QRadioButton(
            "X1, X2, X3..."
        )

        self.radio_custom = QRadioButton(
            "Personalizado"
        )

        self.radio_abc.setChecked(
            True
        )

        self.name_group = QButtonGroup(
            self
        )

        self.name_group.addButton(
            self.radio_abc
        )

        self.name_group.addButton(
            self.radio_x
        )

        self.name_group.addButton(
            self.radio_custom
        )

        radio_row.addWidget(
            self.radio_abc
        )

        radio_row.addWidget(
            self.radio_x
        )

        radio_row.addWidget(
            self.radio_custom
        )

        radio_row.addStretch()

        config_layout.addLayout(
            radio_row
        )

        # ----------------------------------------------------------
        # Campos de nombres
        # ----------------------------------------------------------

        self.names_layout = QGridLayout()

        self.names_layout.setHorizontalSpacing(
            10
        )

        self.names_layout.setVerticalSpacing(
            6
        )

        config_layout.addLayout(
            self.names_layout
        )

        layout.addWidget(
            config_box
        )

        # ==========================================================
        # FUNCIÓN LÓGICA
        # ==========================================================

        function_box = QGroupBox(
            "Función lógica"
        )

        function_box.setObjectName(
            "card_panel"
        )

        function_layout = QVBoxLayout(
            function_box
        )

        function_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        function_layout.setSpacing(10)

        # ----------------------------------------------------------
        # Expresión
        # ----------------------------------------------------------

        self.expr = QLineEdit()

        self.expr.setObjectName(
            "expression_input"
        )

        self.expr.setPlaceholderText(
            "Ejemplo: A'B + AC  o  Σm(1,3,5,7)"
        )

        function_layout.addWidget(
            self.expr
        )

        # ----------------------------------------------------------
        # Información
        # ----------------------------------------------------------

        info = QLabel(
            "Operadores admitidos: + (OR), · o * (AND), "
            "' o ~ (NOT)."
        )

        info.setObjectName(
            "info_label"
        )

        info.setWordWrap(
            True
        )

        function_layout.addWidget(
            info
        )

        # ----------------------------------------------------------
        # Fila inferior
        # ----------------------------------------------------------

        bottom_row = QHBoxLayout()

        bottom_row.setSpacing(
            8
        )

        bottom_row.addWidget(
            QLabel("Tipo de entrada:")
        )

        self.mode = QComboBox()

        self.mode.addItems([
            "Expresión booleana",
            "Minterms"
        ])

        self.mode.setFixedWidth(
            180
        )

        bottom_row.addWidget(
            self.mode
        )

        bottom_row.addStretch()

        # ----------------------------------------------------------
        # Botón limpiar
        # ----------------------------------------------------------

        self.clear = QPushButton(
            "Limpiar"
        )

        self.clear.setObjectName(
            "btn_secondary"
        )

        self.clear.setMinimumWidth(
            90
        )

        # ----------------------------------------------------------
        # Botón procesar
        # ----------------------------------------------------------

        self.process = QPushButton(
            "Procesar"
        )

        self.process.setObjectName(
            "btn_primary"
        )

        self.process.setMinimumWidth(
            100
        )

        bottom_row.addWidget(
            self.clear
        )

        bottom_row.addWidget(
            self.process
        )

        function_layout.addLayout(
            bottom_row
        )

        layout.addWidget(
            function_box
        )

        layout.addStretch()

        # ==========================================================
        # EVENTOS
        # ==========================================================

        self.number_inputs.valueChanged.connect(
            self.update_variable_fields
        )

        self.radio_abc.toggled.connect(
            self.update_variable_fields
        )

        self.radio_x.toggled.connect(
            self.update_variable_fields
        )

        self.radio_custom.toggled.connect(
            self.update_variable_fields
        )

        # ==========================================================
        # CAMPOS INICIALES
        # ==========================================================

        self.update_variable_fields()

    # ==============================================================
    # CAMPOS DE VARIABLES
    # ==============================================================

    def update_variable_fields(self):

        # ----------------------------------------------------------
        # Eliminar campos anteriores
        # ----------------------------------------------------------

        for edit in self.variable_edits:

            edit.deleteLater()

        self.variable_edits.clear()

        while self.names_layout.count():

            item = self.names_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        # ----------------------------------------------------------
        # Número de variables
        # ----------------------------------------------------------

        n = self.number_inputs.value()

        # ----------------------------------------------------------
        # Generar nombres
        # ----------------------------------------------------------

        if self.radio_abc.isChecked():

            names = [
                chr(ord("A") + i)
                for i in range(n)
            ]

        elif self.radio_x.isChecked():

            names = [
                f"X{i + 1}"
                for i in range(n)
            ]

        else:

            names = [
                chr(ord("A") + i)
                for i in range(n)
            ]

        # ----------------------------------------------------------
        # Crear campos
        # ----------------------------------------------------------

        for i, name in enumerate(names):

            edit = QLineEdit(name)

            edit.setObjectName(
                "variable_input"
            )

            edit.setMaximumWidth(
                100
            )

            self.variable_edits.append(
                edit
            )

            self.names_layout.addWidget(
                edit,
                0,
                i
            )

            if not self.radio_custom.isChecked():

                edit.setReadOnly(
                    True
                )

    # ==============================================================
    # OBTENER VARIABLES
    # ==============================================================

    def get_variables(self):

        variables = []

        for edit in self.variable_edits:

            name = edit.text().strip()

            if name:

                variables.append(
                    name
                )

        return variables