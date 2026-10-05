import shutil
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QScrollArea,
    QSizePolicy,
    QFrame
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from logic.karnaugh_solver import (
    build_kmap,
    kmap_labels,
    grouping_candidates
)


class KarnaughWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.current_path = None

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

        root.setSpacing(10)

        # ==========================================================
        # ENCABEZADO
        # ==========================================================

        top = QHBoxLayout()

        top.setContentsMargins(
            2,
            0,
            2,
            0
        )

        self.title = QLabel(
            "Mapa de Karnaugh"
        )

        self.title.setObjectName(
            "kmap_title"
        )

        self.save = QPushButton(
            "Guardar imagen"
        )

        self.save.setObjectName(
            "btn_secondary"
        )

        top.addWidget(
            self.title
        )

        top.addStretch()

        top.addWidget(
            self.save
        )

        root.addLayout(
            top
        )

        # ==========================================================
        # ÁREA DEL MAPA
        # ==========================================================

        self.image = QLabel()

        self.image.setAlignment(
            Qt.AlignCenter
        )

        self.image.setObjectName(
            "kmap_image"
        )

        self.image.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.image.setMinimumSize(
            0,
            0
        )

        self.image_area = QScrollArea()

        self.image_area.setObjectName(
            "kmap_scroll"
        )

        self.image_area.setWidgetResizable(
            True
        )

        self.image_area.setAlignment(
            Qt.AlignCenter
        )

        self.image_area.setFrameShape(
            QFrame.NoFrame
        )

        self.image_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.image_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.image_area.setWidget(
            self.image
        )

        root.addWidget(
            self.image_area,
            1
        )

        # ==========================================================
        # EVENTOS
        # ==========================================================

        self.save.clicked.connect(
            self.save_image
        )

    # ==============================================================
    # DIBUJAR AGRUPACIONES
    # ==============================================================

    def _draw_groupings(
        self,
        ax,
        groups
    ):

        colors = [
            "#e74c3c",
            "#3498db",
            "#2ecc71",
            "#f39c12",
            "#9b59b6",
            "#1abc9c",
            "#e84393",
            "#795548"
        ]

        for group_index, group in enumerate(
            groups
        ):

            cells = group.get(
                "cells",
                []
            )

            if not cells:
                continue

            color = colors[
                group_index % len(colors)
            ]

            # ------------------------------------------------------
            # Normalizar celdas
            # ------------------------------------------------------

            normalized_cells = set()

            for cell in cells:

                if len(cell) < 2:
                    continue

                r = int(cell[0])
                c = int(cell[1])

                normalized_cells.add(
                    (r, c)
                )

            if not normalized_cells:
                continue

            # ------------------------------------------------------
            # Separar componentes visuales
            #
            # Esto permite dibujar correctamente grupos que
            # cruzan los bordes del mapa.
            # ------------------------------------------------------

            components = []

            remaining = set(
                normalized_cells
            )

            while remaining:

                start = next(
                    iter(remaining)
                )

                component = {
                    start
                }

                queue = [
                    start
                ]

                remaining.remove(
                    start
                )

                while queue:

                    r, c = queue.pop()

                    neighbors = [
                        (r - 1, c),
                        (r + 1, c),
                        (r, c - 1),
                        (r, c + 1)
                    ]

                    for neighbor in neighbors:

                        if neighbor in remaining:

                            remaining.remove(
                                neighbor
                            )

                            component.add(
                                neighbor
                            )

                            queue.append(
                                neighbor
                            )

                components.append(
                    component
                )

            # ------------------------------------------------------
            # Dibujar cada componente
            # ------------------------------------------------------

            for component in components:

                rows_group = [
                    cell[0]
                    for cell in component
                ]

                cols_group = [
                    cell[1]
                    for cell in component
                ]

                min_row = min(
                    rows_group
                )

                max_row = max(
                    rows_group
                )

                min_col = min(
                    cols_group
                )

                max_col = max(
                    cols_group
                )

                # --------------------------------------------------
                # Centro
                # --------------------------------------------------

                center_x = (
                    min_col + max_col
                ) / 2 + 0.5

                center_y = (
                    min_row + max_row
                ) / 2 + 0.5

                # --------------------------------------------------
                # Dimensiones
                # --------------------------------------------------

                group_width = (
                    max_col - min_col + 1
                )

                group_height = (
                    max_row - min_row + 1
                )

                # --------------------------------------------------
                # Óvalo
                # --------------------------------------------------

                ellipse = Ellipse(
                    (
                        center_x,
                        center_y
                    ),
                    width=group_width * 0.88,
                    height=group_height * 0.72,
                    fill=False,
                    edgecolor=color,
                    linewidth=3.0,
                    zorder=10
                )

                ax.add_patch(
                    ellipse
                )

    # ==============================================================
    # GENERAR MAPA
    # ==============================================================

    def update_map(
        self,
        variables,
        minterms
    ):

        # ==========================================================
        # LÍMITE DE VARIABLES
        # ==========================================================

        if len(variables) > 4:

            self.current_path = None

            self.image.clear()

            self.image.setText(
                "El mapa gráfico está limitado "
                "a 4 variables.\n"
                "La simplificación continúa funcionando."
            )

            return

        try:

            # ======================================================
            # CONSTRUIR DATOS
            # ======================================================

            _, data = build_kmap(
                len(variables),
                minterms
            )

            row_variables, col_variables, rows, cols = (
                kmap_labels(
                    variables
                )
            )

            # ======================================================
            # AGRUPACIONES
            # ======================================================

            groups = grouping_candidates(
                len(variables),
                minterms
            )

            # ======================================================
            # CREAR FIGURA
            # ======================================================

            fig, ax = plt.subplots(
                figsize=(6.5, 4.5),
                dpi=150
            )

            fig.patch.set_facecolor(
                "#252526"
            )

            ax.set_facecolor(
                "#252526"
            )

            ax.set_xlim(
                0,
                len(cols)
            )

            ax.set_ylim(
                0,
                len(rows)
            )

            # ======================================================
            # ETIQUETAS
            # ======================================================

            ax.set_xticks(
                [
                    i + 0.5
                    for i in range(
                        len(cols)
                    )
                ],
                cols
            )

            ax.set_yticks(
                [
                    i + 0.5
                    for i in range(
                        len(rows)
                    )
                ],
                rows
            )

            ax.invert_yaxis()

            # ======================================================
            # NOMBRES DE VARIABLES
            # ======================================================

            ax.set_xlabel(
                f"{''.join(col_variables)} (Gray)",
                color="#CCCCCC"
            )

            ax.set_ylabel(
                f"{''.join(row_variables)} (Gray)",
                color="#CCCCCC"
            )

            # ======================================================
            # EJES
            # ======================================================

            ax.tick_params(
                colors="#CCCCCC"
            )

            for spine in ax.spines.values():

                spine.set_color(
                    "#555555"
                )

            # ======================================================
            # VALORES DEL MAPA
            # ======================================================

            for (r, c), (value, m) in data.items():

                # Valor
                ax.text(
                    c + 0.5,
                    r + 0.5,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="#FFFFFF",
                    zorder=4
                )

                # Minterm
                ax.text(
                    c + 0.12,
                    r + 0.12,
                    str(m),
                    ha="left",
                    va="top",
                    fontsize=8,
                    color="#AAAAAA",
                    zorder=4
                )

            # ======================================================
            # CUADRÍCULA
            # ======================================================

            ax.set_xticks(
                range(
                    len(cols) + 1
                ),
                minor=True
            )

            ax.set_yticks(
                range(
                    len(rows) + 1
                ),
                minor=True
            )

            ax.grid(
                which="minor",
                linewidth=1.2,
                color="#555555",
                zorder=1
            )

            ax.grid(
                False,
                which="major"
            )

            # ======================================================
            # DIBUJAR SOLO LAS AGRUPACIONES
            # ======================================================

            self._draw_groupings(
                ax,
                groups
            )

            # ======================================================
            # TÍTULO
            # ======================================================

            ax.set_title(
                "Mapa de Karnaugh",
                color="#FFFFFF",
                fontsize=13,
                fontweight="bold",
                pad=12
            )

            # ======================================================
            # AJUSTAR
            # ======================================================

            fig.tight_layout(
                pad=1.2
            )

            # ======================================================
            # GUARDAR IMAGEN TEMPORAL
            # ======================================================

            path = (
                Path(
                    tempfile.gettempdir()
                )
                / "karnaugh_actual.png"
            )

            fig.savefig(
                path,
                dpi=180,
                bbox_inches="tight",
                facecolor=fig.get_facecolor()
            )

            plt.close(
                fig
            )

            self.current_path = str(
                path
            )

            # ======================================================
            # MOSTRAR
            # ======================================================

            self._update_pixmap()

        except Exception as exc:

            self.current_path = None

            self.image.clear()

            self.image.setText(
                "No se pudo generar el mapa "
                f"de Karnaugh:\n{exc}"
            )

    # ==============================================================
    # REDIMENSIONAR
    # ==============================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        if self.current_path:

            self._update_pixmap()

    # ==============================================================
    # ESCALAR MAPA
    # ==============================================================

    def _update_pixmap(self):

        if not self.current_path:
            return

        pixmap = QPixmap(
            self.current_path
        )

        if pixmap.isNull():
            return

        viewport = (
            self.image_area
            .viewport()
        )

        width = max(
            100,
            viewport.width() - 20
        )

        height = max(
            100,
            viewport.height() - 20
        )

        scaled = pixmap.scaled(
            width,
            height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.image.setPixmap(
            scaled
        )

    # ==============================================================
    # GUARDAR IMAGEN
    # ==============================================================

    def save_image(self):

        if not self.current_path:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar mapa de Karnaugh",
            "karnaugh.png",
            "PNG (*.png)"
        )

        if path:

            shutil.copy2(
                self.current_path,
                path
            )