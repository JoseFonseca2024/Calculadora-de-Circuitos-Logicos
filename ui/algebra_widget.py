from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt


class AlgebraWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        # ==========================================================
        # LAYOUT PRINCIPAL
        # ==========================================================

        root = QVBoxLayout(self)

        root.setContentsMargins(
            12,
            12,
            12,
            12
        )

        root.setSpacing(12)

        # ==========================================================
        # CONTENEDOR PRINCIPAL
        # ==========================================================

        box = QGroupBox(
            "Procedimiento de Álgebra Booleana"
        )

        box.setObjectName(
            "card_panel"
        )

        box_layout = QVBoxLayout(
            box
        )

        box_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        box_layout.setSpacing(
            10
        )

        # ==========================================================
        # FUNCIÓN ORIGINAL
        # ==========================================================

        original_title = QLabel(
            "FUNCIÓN ORIGINAL"
        )

        original_title.setObjectName(
            "section_title"
        )

        box_layout.addWidget(
            original_title
        )

        self.original = QLabel()

        self.original.setObjectName(
            "expression_display"
        )

        self.original.setWordWrap(
            True
        )

        self.original.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        box_layout.addWidget(
            self.original
        )

        # ==========================================================
        # PROCEDIMIENTO
        # ==========================================================

        procedure_title = QLabel(
            "PROCEDIMIENTO"
        )

        procedure_title.setObjectName(
            "section_title"
        )

        box_layout.addWidget(
            procedure_title
        )

        # Área desplazable
        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.content = QWidget()

        self.content.setObjectName(
            "steps_container"
        )

        self.steps_layout = QVBoxLayout(
            self.content
        )

        self.steps_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.steps_layout.setSpacing(
            8
        )

        self.scroll.setWidget(
            self.content
        )

        box_layout.addWidget(
            self.scroll,
            1
        )

        # ==========================================================
        # RESULTADO
        # ==========================================================

        result_title = QLabel(
            "RESULTADO"
        )

        result_title.setObjectName(
            "section_title"
        )

        box_layout.addWidget(
            result_title
        )

        self.result = QLabel()

        self.result.setObjectName(
            "result_display"
        )

        self.result.setWordWrap(
            True
        )

        self.result.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        box_layout.addWidget(
            self.result
        )

        root.addWidget(
            box,
            1
        )

    # ==============================================================
    # ACTUALIZAR PROCEDIMIENTO
    # ==============================================================

    def update_steps(
        self,
        original,
        simplified,
        steps
    ):

        # ==========================================================
        # FUNCIÓN ORIGINAL
        # ==========================================================

        self.original.setText(
            str(original)
        )

        # ==========================================================
        # RESULTADO
        # ==========================================================

        self.result.setText(
            f"F = {simplified}"
        )

        # ==========================================================
        # LIMPIAR PASOS ANTERIORES
        # ==========================================================

        while self.steps_layout.count():

            item = self.steps_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        # ==========================================================
        # CREAR PASOS
        # ==========================================================

        for name, expr, law in steps:

            step_frame = QFrame()

            step_frame.setObjectName(
                "step_card"
            )

            step_layout = QVBoxLayout(
                step_frame
            )

            step_layout.setContentsMargins(
                12,
                10,
                12,
                10
            )

            step_layout.setSpacing(
                5
            )

            # ------------------------------------------------------
            # Nombre del paso
            # ------------------------------------------------------

            step_name = QLabel(
                name
            )

            step_name.setObjectName(
                "step_name"
            )

            step_layout.addWidget(
                step_name
            )

            # ------------------------------------------------------
            # Expresión
            # ------------------------------------------------------

            expression = QLabel(
                f"F = {expr}"
            )

            expression.setObjectName(
                "step_expression"
            )

            expression.setWordWrap(
                True
            )

            Qt.TextSelectableByMouse

            step_layout.addWidget(
                expression
            )

            # ------------------------------------------------------
            # Ley aplicada
            # ------------------------------------------------------

            law_label = QLabel(
                law
            )

            law_label.setObjectName(
                "step_law"
            )

            law_label.setWordWrap(
                True
            )

            step_layout.addWidget(
                law_label
            )

            self.steps_layout.addWidget(
                step_frame
            )

        # ==========================================================
        # ESPACIO FINAL
        # ==========================================================

        self.steps_layout.addStretch()