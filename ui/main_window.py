from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QMessageBox,
    QFileDialog
)

from PySide6.QtGui import QAction
from sympy import symbols
from utils.constants import APP_TITLE, DEFAULT_VARIABLES, MAX_VARIABLES
from utils.validators import validate_variable_names
from logic.parser import parse_expression, parse_minterms
from logic.boolean_engine import simplify_expression, expression_to_text
from logic.truth_table import generate_truth_table, minterms_from_expression
from logic.verifier import verify
from logic.algebra_solver import build_steps
from ui.input_widget import InputWidget
from ui.truth_table_widget import TruthTableWidget
from ui.algebra_widget import AlgebraWidget
from ui.karnaugh_widget import KarnaughWidget
from exports.exporter import export_txt, export_pdf

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1180, 500)
        self.setMinimumSize(600, 200)
        self.variables = DEFAULT_VARIABLES[:4]
        self.original = None
        self.simplified = None
        self.minterms = []
        self._build_ui()

    def _build_ui(self):

        # ==========================================================
        # MENÚ PRINCIPAL
        # ==========================================================

        self._menus()

        # ==========================================================
        # NAVEGACIÓN
        # ==========================================================

        self.tabs = QTabWidget()

        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)
        self.tabs.setUsesScrollButtons(False)

        # ==========================================================
        # WIDGETS
        # ==========================================================

        self.input = InputWidget()
        self.truth = TruthTableWidget()
        self.algebra = AlgebraWidget()
        self.kmap = KarnaughWidget()

        # ==========================================================
        # PESTAÑAS
        # ==========================================================

        self.tabs.addTab(
            self.input,
            "Entrada"
        )

        self.tabs.addTab(
            self.truth,
            "Tabla de Verdad"
        )

        self.tabs.addTab(
            self.algebra,
            "Álgebra"
        )

        self.tabs.addTab(
            self.kmap,
            "Karnaugh"
        )

        self.setCentralWidget(
            self.tabs
        )

        # ==========================================================
        # STATUS BAR
        # ==========================================================

        self.statusBar().showMessage(
            "Listo. Introduzca una función y pulse Procesar."
        )

        # ==========================================================
        # CONEXIONES
        # ==========================================================

        self.input.process.clicked.connect(
            self.process
        )

        self.input.clear.clicked.connect(
            self.clear_all
        )

        # ==========================================================
        # ESTILO
        # ==========================================================

        self._apply_style()

    def _menus(self):
        mb=self.menuBar()
        archivo=mb.addMenu("Archivo")
        self._action(archivo,"Nueva función",self.clear_all)
        self._action(archivo,"Abrir",self.open_file)
        self._action(archivo,"Guardar",self.save_file)
        self._action(archivo,"Exportar procedimiento",self.export_procedure)
        archivo.addSeparator()
        self._action(archivo,"Salir",self.close)
        herramientas=mb.addMenu("Herramientas")
        self._action(herramientas,"Tabla de verdad",lambda:self.tabs.setCurrentIndex(1))
        self._action(herramientas,"Álgebra Booleana",lambda:self.tabs.setCurrentIndex(2))
        self._action(herramientas,"Karnaugh",lambda:self.tabs.setCurrentIndex(3))
        herramientas.addSeparator()
        ayuda=mb.addMenu("Ayuda")
        self._action(ayuda,"Manual",self.manual)
        self._action(ayuda,"Acerca de",self.about)

    def _action(self,menu,text,slot):
        a=QAction(text,self); a.triggered.connect(slot); menu.addAction(a); return a

    def _apply_style(self):

        self.setStyleSheet("""

            /* ======================================================
            GLOBAL
            ====================================================== */

            QMainWindow,
            QWidget {

                background-color: #1E1E1E;
                color: #E6E6E6;

                font-family:
                    "Segoe UI",
                    "Roboto",
                    "Helvetica",
                    sans-serif;

                font-size: 13px;
            }


            /* ======================================================
            MENÚ
            ====================================================== */

            QMenuBar {

                background-color: #1E1E1E;

                color: #DADADA;

                border: none;

                padding: 3px 6px;
            }

            QMenuBar::item {

                background: transparent;

                padding:
                    6px
                    10px;
            }

            QMenuBar::item:selected {

                background-color: #2A2A2A;

                border-radius: 5px;
            }

            QMenu {

                background-color: #252526;

                color: #E6E6E6;

                border: 1px solid #3A3A3A;

                padding: 5px;
            }

            QMenu::item {

                padding:
                    7px
                    25px
                    7px
                    12px;
            }

            QMenu::item:selected {

                background-color: #333333;

                color: #FFFFFF;
            }


            /* ======================================================
            PESTAÑAS
            ====================================================== */

            QTabWidget::pane {

                background-color: #1E1E1E;

                border: none;
            }

            QTabBar {

                background-color: #1E1E1E;
            }

            QTabBar::tab {

                background-color: transparent;

                color: #8F8F8F;

                border: none;

                padding:
                    10px
                    16px;

                margin-right: 2px;

                font-size: 13px;
            }

            QTabBar::tab:hover {

                color: #FFFFFF;

                background-color: #292929;

                border-radius: 5px;
            }

            QTabBar::tab:selected {

                color: #81C784;

                background-color: #252526;

                border-bottom:
                    2px solid #81C784;

                font-weight: 600;
            }


            /* ======================================================
            GROUP BOX
            ====================================================== */

            QGroupBox {

                background-color: #252526;

                border:
                    1px solid #363636;

                border-radius: 8px;

                margin-top: 12px;

                padding:
                    18px
                    10px
                    10px
                    10px;
            }

            QGroupBox::title {

                subcontrol-origin: margin;

                left: 12px;

                padding:
                    0
                    6px;

                color: #FFFFFF;

                font-weight: 600;

                background-color: #252526;
            }


            /* ======================================================
            LABELS
            ====================================================== */

            QLabel {

                color: #DADADA;
            }


            /* ======================================================
            CAMPOS DE TEXTO
            ====================================================== */

            QLineEdit {

                background-color: #2D2D30;

                color: #FFFFFF;

                border:
                    1px solid #3E3E42;

                border-radius: 5px;

                padding:
                    7px
                    10px;
            }

            QLineEdit:hover {

                border:
                    1px solid #555555;
            }

            QLineEdit:focus {

                border:
                    1px solid #81C784;
            }


            /* ======================================================
            COMBOBOX
            ====================================================== */

            QComboBox {

                background-color: #2D2D30;

                color: #FFFFFF;

                border:
                    1px solid #3E3E42;

                border-radius: 5px;

                padding:
                    7px
                    10px;
            }

            QComboBox:hover {

                border:
                    1px solid #555555;
            }

            QComboBox:focus {

                border:
                    1px solid #81C784;
            }

            QComboBox::drop-down {

                border: none;

                width: 25px;
            }

            QComboBox QAbstractItemView {

                background-color: #252526;

                color: #FFFFFF;

                selection-background-color: #333333;

                border:
                    1px solid #3E3E42;
            }


            /* ======================================================
            RADIO BUTTONS
            ====================================================== */

            QRadioButton {

                color: #DADADA;

                spacing: 8px;
            }

            QRadioButton::indicator {

                width: 14px;

                height: 14px;

                border-radius: 7px;

                border:
                    2px solid #666666;

                background-color: transparent;
            }

            QRadioButton::indicator:checked {

                border:
                    2px solid #81C784;

                background-color: #81C784;
            }


            /* ======================================================
            BOTONES
            ====================================================== */

            QPushButton {

                background-color: #303030;

                color: #E6E6E6;

                border:
                    1px solid #454545;

                border-radius: 5px;

                padding:
                    7px
                    16px;
            }

            QPushButton:hover {

                background-color: #383838;

                border:
                    1px solid #666666;
            }

            QPushButton:pressed {

                background-color: #292929;
            }


            /* ======================================================
            BOTÓN PRINCIPAL
            ====================================================== */

            QPushButton#btn_primary {

                background-color: #81C784;

                color: #121212;

                border: none;

                font-weight: 600;

                padding:
                    8px
                    22px;
            }

            QPushButton#btn_primary:hover {

                background-color: #A5D6A7;
            }


            /* ======================================================
            BOTÓN SECUNDARIO
            ====================================================== */

            QPushButton#btn_secondary {

                background-color: transparent;

                color: #E0E0E0;

                border:
                    1px solid #555555;

                padding:
                    8px
                    22px;
            }

            QPushButton#btn_secondary:hover {

                background-color: #333333;

                border:
                    1px solid #777777;
            }


            /* ======================================================
            STATUS BAR
            ====================================================== */

            QStatusBar {

                background-color: #181818;

                color: #AAAAAA;

                border-top:
                    1px solid #303030;

                padding:
                    3px
                    8px;
            }


            /* ======================================================
            SCROLLBARS
            ====================================================== */

            QScrollBar:vertical {

                background-color: #202020;

                width: 10px;

                margin: 0;
            }

            QScrollBar::handle:vertical {

                background-color: #4A4A4A;

                border-radius: 5px;

                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {

                background-color: #666666;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {

                height: 0;
            }

            QScrollBar:horizontal {

                background-color: #202020;

                height: 10px;

                margin: 0;
            }

            QScrollBar::handle:horizontal {

                background-color: #4A4A4A;

                border-radius: 5px;

                min-width: 30px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {

                width: 0;
            }

            /* ======================================================
            TÍTULOS DE SECCIÓN
            ====================================================== */

            QLabel#section_title {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
                padding-top: 4px;
                padding-bottom: 2px;
            }


            /* ======================================================
            EXPRESIÓN ORIGINAL
            ====================================================== */

            QLabel#expression_display {
                background-color: #202020;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 10px;
                color: #E6E6E6;
            }


            /* ======================================================
            CONTENEDOR DE PASOS
            ====================================================== */

            QWidget#steps_container {
                background-color: transparent;
            }


            /* ======================================================
            TARJETA DE PASO
            ====================================================== */

            QFrame#step_card {
                background-color: #202020;
                border: 1px solid #343434;
                border-radius: 6px;
            }


            /* ======================================================
            NOMBRE DEL PASO
            ====================================================== */

            QLabel#step_name {
                color: #81C784;
                font-weight: 700;
                font-size: 13px;
            }


            /* ======================================================
            EXPRESIÓN DEL PASO
            ====================================================== */

            QLabel#step_expression {
                color: #F0F0F0;
                font-size: 13px;
                padding: 2px 0;
            }


            /* ======================================================
            LEY APLICADA
            ====================================================== */

            QLabel#step_law {
                color: #AAAAAA;
                font-size: 12px;
                font-style: italic;
            }


            /* ======================================================
            RESULTADO
            ====================================================== */

            QLabel#result_display {
                background-color: #26342A;
                border: 1px solid #4C7A55;
                border-radius: 6px;
                padding: 10px;
                color: #A5D6A7;
                font-size: 15px;
                font-weight: 700;
            }

            /* ======================================================
            TABLA DE VERDAD
            ====================================================== */

            QLabel#truth_title {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 700;
                padding-bottom: 2px;
            }

            QFrame#verification_panel {
                background-color: #26342A;
                border: 1px solid #4C7A55;
                border-radius: 7px;
            }

            QLabel#verification_status {
                color: #A5D6A7;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0;
            }


            /* ------------------------------------------------------
            TABLA
            ------------------------------------------------------ */

            QTableWidget {
                background-color: #252526;
                alternate-background-color: #202020;

                color: #E6E6E6;

                border: 1px solid #363636;
                border-radius: 7px;

                gridline-color: #3A3A3A;

                font-size: 13px;

                selection-background-color: transparent;
                selection-color: #E6E6E6;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QTableWidget::item:hover {
                background-color: #2D2D30;
            }


            /* ------------------------------------------------------
            ENCABEZADO
            ------------------------------------------------------ */

            QHeaderView::section {
                background-color: #2D2D30;

                color: #FFFFFF;

                border: none;
                border-right: 1px solid #3A3A3A;
                border-bottom: 1px solid #3A3A3A;

                padding: 8px;

                font-weight: 700;

                text-align: center;
            }


            /* ------------------------------------------------------
            ENCABEZADO VERTICAL
            ------------------------------------------------------ */

            QHeaderView:vertical {
                background-color: #202020;
            }

            QHeaderView::section:vertical {
                background-color: #202020;

                color: #777777;

                border: none;
                border-right: 1px solid #333333;
                border-bottom: 1px solid #333333;

                font-size: 11px;
            }

            /* ======================================================
            KARNAUGH
            ====================================================== */

            QLabel#kmap_title {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 700;
            }

            QScrollArea#kmap_scroll {
                background-color: #252526;
                border: 1px solid #333333;
                border-radius: 8px;
            }

            QLabel#kmap_image {
                background-color: #252526;
            }

            QFrame#kmap_groups_panel {
                background-color: #252526;
                border: 1px solid #333333;
                border-radius: 8px;
            }

            QScrollArea#kmap_groups_scroll {
                background-color: transparent;
                border: none;
            }

            QLabel#kmap_groups {
                color: #DADADA;
                background-color: transparent;
                padding: 4px;
            }

        """)


    def process(self):

        text = self.input.expr.text().strip()

        if not text:
            QMessageBox.warning(
                self,
                "Entrada",
                "Introduzca una función."
            )
            return

        try:

            # ======================================================
            # OBTENER VARIABLES DESDE LA PANTALLA PRINCIPAL
            # ======================================================

            self.variables = self.input.get_variables()

            if not self.variables:
                raise ValueError(
                    "Debe configurar al menos una entrada."
                )

            if len(self.variables) > MAX_VARIABLES:
                raise ValueError(
                    f"Máximo {MAX_VARIABLES} entradas."
                )

            # ======================================================
            # VALIDAR NOMBRES
            # ======================================================

            self.variables = validate_variable_names(
                self.variables
            )

            # ======================================================
            # CREAR SÍMBOLOS
            # ======================================================

            syms = [
                symbols(v, boolean=True)
                for v in self.variables
            ]

            # ======================================================
            # PARSEAR FUNCIÓN
            # ======================================================

            if self.input.mode.currentIndex() == 1:

                self.original, self.minterms = parse_minterms(
                    text,
                    self.variables
                )

            else:

                self.original = parse_expression(
                    text,
                    self.variables
                )

                self.minterms = minterms_from_expression(
                    self.original,
                    syms
                )

            # ======================================================
            # SIMPLIFICAR
            # ======================================================

            self.simplified = simplify_expression(
                self.original
            )

            # ======================================================
            # TABLA DE VERDAD
            # ======================================================

            rows = generate_truth_table(
                self.original,
                self.simplified,
                syms
            )

            self.truth.update_table(
                self.variables,
                rows
            )

            # ======================================================
            # ÁLGEBRA
            # ======================================================

            steps = build_steps(
                self.original,
                self.simplified
            )

            self.algebra.update_steps(
                self.original,
                self.simplified,
                steps
            )

            # ======================================================
            # KARNAUGH
            # ======================================================

            self.kmap.update_map(
                self.variables,
                self.minterms
            )

            # ======================================================
            # VERIFICACIÓN
            # ======================================================

            ok = verify(
                self.original,
                self.simplified
            )

            if ok:

                self.statusBar().showMessage(
                    "✓ Procesamiento completado. "
                    "Funciones equivalentes."
                )

            else:

                self.statusBar().showMessage(
                    "⚠ Verificación fallida."
                )

            # Ir a tabla
            self.tabs.setCurrentIndex(1)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error al procesar",
                str(e)
            )

    def clear_all(self):
        self.input.expr.clear()
        self.original=self.simplified=None
        self.minterms=[]
        self.statusBar().showMessage("Formulario limpiado.")

    def open_file(self):
        path,_=QFileDialog.getOpenFileName(self,"Abrir función","","Archivos de texto (*.txt);;Todos (*.*)")
        if path:
            self.input.expr.setText(Path(path).read_text(encoding="utf-8"))

    def save_file(self):
        path,_=QFileDialog.getSaveFileName(self,"Guardar función","","Texto (*.txt)")
        if path:
            Path(path).write_text(self.input.expr.text(),encoding="utf-8")

    def export_procedure(self):
        if self.original is None:
            QMessageBox.information(self,"Exportar","Primero procese una función.")
            return
        path,_=QFileDialog.getSaveFileName(self,"Exportar procedimiento","","PDF (*.pdf);;Texto (*.txt)")
        if not path:return
        steps=build_steps(self.original,self.simplified)
        verified=verify(self.original,self.simplified)
        if path.lower().endswith(".pdf"):
            export_pdf(path,expression_to_text(self.original),expression_to_text(self.simplified),steps,self.minterms,verified)
        else:
            export_txt(path,expression_to_text(self.original),expression_to_text(self.simplified),steps,self.minterms,verified)
        QMessageBox.information(self,"Exportación","Archivo exportado correctamente.")

    def manual(self):

        QMessageBox.information(
            self,
            "Manual",
            "1. Configure el número y nombre de las entradas "
            "desde la pestaña Entrada.\n"
            "2. Introduzca una expresión booleana o minterms.\n"
            "3. Pulse Procesar.\n"
            "4. Revise la tabla de verdad, el procedimiento "
            "algebraico y el mapa de Karnaugh.\n"
            "5. Use Archivo > Exportar procedimiento para "
            "generar un PDF o TXT."
        )

    def about(self):
        QMessageBox.about(self,APP_TITLE,
            "Herramienta educativa local para simplificación de circuitos lógicos.\n"
            "Python 3.12+ · PySide6 · SymPy · Matplotlib · NetworkX")
