from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QHeaderView,
    QSizePolicy,
    QFrame
)

from PySide6.QtCore import Qt


class TruthTableWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

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

        root.setSpacing(
            10
        )

        # ==========================================================
        # TÍTULO
        # ==========================================================

        title = QLabel(
            "Tabla de Verdad"
        )

        title.setObjectName(
            "truth_title"
        )

        root.addWidget(
            title
        )

        # ==========================================================
        # ESTADO DE VERIFICACIÓN
        # ==========================================================

        self.status_frame = QFrame()

        self.status_frame.setObjectName(
            "verification_panel"
        )

        status_layout = QHBoxLayout(
            self.status_frame
        )

        status_layout.setContentsMargins(
            10,
            7,
            10,
            7
        )

        self.status = QLabel()

        self.status.setObjectName(
            "verification_status"
        )

        self.status.setWordWrap(
            True
        )

        status_layout.addWidget(
            self.status
        )

        root.addWidget(
            self.status_frame
        )

        # ==========================================================
        # TABLA
        # ==========================================================

        self.table = QTableWidget()

        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.NoSelection
        )

        self.table.setFocusPolicy(
            Qt.NoFocus
        )

        self.table.setShowGrid(
            True
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setWordWrap(
            False
        )

        # Scrollbars solamente cuando sean necesarias
        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # ==========================================================
        # ENCABEZADO HORIZONTAL
        # ==========================================================

        horizontal_header = (
            self.table.horizontalHeader()
        )

        horizontal_header.setSectionResizeMode(
            QHeaderView.Fixed
        )

        horizontal_header.setDefaultAlignment(
            Qt.AlignCenter
        )

        horizontal_header.setMinimumSectionSize(
            55
        )

        # ==========================================================
        # ENCABEZADO VERTICAL
        # ==========================================================

        vertical_header = (
            self.table.verticalHeader()
        )

        vertical_header.setSectionResizeMode(
            QHeaderView.Fixed
        )

        vertical_header.setDefaultSectionSize(
            32
        )

        vertical_header.setVisible(
            True
        )

        # ==========================================================
        # LAYOUT
        # ==========================================================

        root.addWidget(
            self.table,
            1
        )

    # ==============================================================
    # ACTUALIZAR TABLA
    # ==============================================================

    def update_table(
        self,
        variables,
        rows
    ):

        self.table.clear()

        # ==========================================================
        # COLUMNAS
        # ==========================================================

        self.table.setColumnCount(
            len(variables) + 1
        )

        self.table.setHorizontalHeaderLabels(
            variables + ["F"]
        )

        self.table.setRowCount(
            len(rows)
        )

        # ==========================================================
        # LLENAR TABLA
        # ==========================================================

        for row_index, (
            bits,
            original,
            simplified
        ) in enumerate(rows):

            # ------------------------------------------------------
            # VARIABLES
            # ------------------------------------------------------

            for column_index, bit in enumerate(
                bits
            ):

                item = QTableWidgetItem(
                    str(bit)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row_index,
                    column_index,
                    item
                )

            # ------------------------------------------------------
            # FUNCIÓN
            # ------------------------------------------------------

            result_item = QTableWidgetItem(
                str(original)
            )

            result_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row_index,
                len(variables),
                result_item
            )

        # ==========================================================
        # ANCHOS
        # ==========================================================

        # Todas las entradas
        for column in range(
            len(variables)
        ):

            self.table.setColumnWidth(
                column,
                65
            )

        # Columna F
        self.table.setColumnWidth(
            len(variables),
            70
        )

        # ==========================================================
        # ALTURA DE FILAS
        # ==========================================================

        for row_index in range(
            self.table.rowCount()
        ):

            self.table.setRowHeight(
                row_index,
                32
            )

        # ==========================================================
        # VERIFICACIÓN
        # ==========================================================

        equivalent = all(
            original == simplified
            for _, original, simplified in rows
        )

        if equivalent:

            self.status.setText(
                "✓ Las funciones son equivalentes."
            )

            self.status_frame.setProperty(
                "state",
                "success"
            )

        else:

            self.status.setText(
                "⚠ Se detectaron diferencias."
            )

            self.status_frame.setProperty(
                "state",
                "warning"
            )

        # Forzar actualización del estilo dinámico
        self.status_frame.style().unpolish(
            self.status_frame
        )

        self.status_frame.style().polish(
            self.status_frame
        )