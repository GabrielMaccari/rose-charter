import matplotlib
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

matplotlib.use("svg")


class MainWindow(QMainWindow):
    column1_ok = True
    column2_ok = True

    def __init__(self, controller):
        self.controller = controller
        super().__init__()
        self.setWindowTitle('Rose Charter')
        self.setWindowIcon(QIcon('icons/windowIcon.ico'))

        y = 5
        self.file_label = QLabel('Selecione um arquivo para começar.', self)
        self.file_label.setGeometry(5, y, 240, 25)

        self.open_file_button = QToolButton(self)
        self.open_file_button.setText("Selecionar")
        self.open_file_button.setGeometry(245, y, 80, 25)
        self.open_file_button.clicked.connect(self.open_file_button_pressed)

        y += 30
        self.divider = QFrame(self)
        self.divider.setGeometry(5, y, 320, 3)
        self.divider.setLineWidth(1)
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)

        y += 10
        self.column1_combo_label = QLabel('Dados para comprimento dos leques (Ex: direção):', self)
        self.column1_combo_label.setGeometry(5, y, 320, 18)
        self.column1_combo_label.setEnabled(False)

        y += 18
        self.column1_combo = QComboBox(self)
        self.column1_combo.setGeometry(5, y, 290, 20)
        self.column1_combo.setEnabled(False)
        self.column1_combo.currentTextChanged.connect(lambda: self.column_selected(1))

        self.column1_check_icon = QLabel("", self)
        self.column1_check_icon.setGeometry(300, y, 20, 20)
        self.column1_check_icon.setPixmap(QPixmap("icons/ok.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        self.column1_check_icon.show()

        y += 30
        self.column2_combo_checkbox = QCheckBox('Dados para divisão dos leques (Ex: velocidade):', self)
        self.column2_combo_checkbox.setGeometry(5, y, 320, 18)
        self.column2_combo_checkbox.clicked.connect(self.enable_column2_combo)
        self.column2_combo_checkbox.setEnabled(False)

        y += 18
        self.column2_combo = QComboBox(self)
        self.column2_combo.setGeometry(5, y, 290, 20)
        self.column2_combo.setEnabled(False)
        self.column2_combo.currentTextChanged.connect(lambda: self.column_selected(2))

        self.column2_check_icon = QLabel("", self)
        self.column2_check_icon.setGeometry(300, y, 20, 20)
        self.column2_check_icon.setPixmap(QPixmap("icons/ok.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        self.column2_check_icon.show()

        y += 30
        self.mirror_checkbox = QCheckBox('Espelhar dados', self)
        self.mirror_checkbox.setGeometry(5, y, 160, 20)
        self.mirror_checkbox.setToolTip(
            'Ao selecionar esta opção, sentidos opostos (ex: E e W) serão '
            'somados e espelhados.'
        )
        self.mirror_checkbox.clicked.connect(self.mirror_checkbox_clicked)

        self.y_axis_checkbox = QCheckBox('Mostrar eixo Y (circular)', self)
        self.y_axis_checkbox.setGeometry(160, y, 160, 20)
        self.y_axis_checkbox.clicked.connect(self.show_y_checkbox_clicked)
        self.y_axis_checkbox.setChecked(True)

        y += 20
        self.x_axis_checkbox = QCheckBox('Mostrar eixo X (radial)', self)
        self.x_axis_checkbox.setGeometry(5, y, 160, 20)
        self.x_axis_checkbox.clicked.connect(self.show_x_checkbox_clicked)
        self.x_axis_checkbox.setChecked(True)

        self.y_labels_checkbox = QCheckBox('Mostrar rótulos de Y', self)
        self.y_labels_checkbox.setGeometry(160, y, 160, 20)
        self.y_labels_checkbox.clicked.connect(self.show_y_labels_checkbox_clicked)
        self.y_labels_checkbox.setChecked(True)

        y += 20
        self.x_labels_checkbox = QCheckBox('Mostrar rótulos de X', self)
        self.x_labels_checkbox.setGeometry(5, y, 160, 20)
        self.x_labels_checkbox.clicked.connect(self.show_x_labels_checkbox_clicked)
        self.x_labels_checkbox.setChecked(True)

        self.color_label = QLabel('Cor dos leques:', self)
        self.color_label.setGeometry(160, y, 150, 20)

        self.color_button = QPushButton('#000000', self)
        self.color_button.setGeometry(245, y, 80, 20)
        self.color_button.setStyleSheet("color: #000000; "
                                        "background-color: #EAEAEA;"
                                        "border-style: None")
        self.color_button.clicked.connect(self.color_button_pressed)

        y += 25
        self.y_labels_position_label = QLabel('Posição dos rótulos de Y (°):', self)
        self.y_labels_position_label.setGeometry(5, y, 150, 20)

        self.y_labels_position_spinbox = QDoubleSpinBox(self)
        self.y_labels_position_spinbox.setGeometry(155, y, 55, 20)
        self.y_labels_position_spinbox.setRange(0, 360)
        self.y_labels_position_spinbox.setValue(56.25)
        self.y_labels_position_spinbox.valueChanged.connect(self.y_labels_position_changed)

        y += 25
        self.sectors_combo_label = QLabel('Setores do diagrama:', self)
        self.sectors_combo_label.setGeometry(5, y, 160, 18)

        y += 18
        self.sectors_combo = QComboBox(self)
        self.sectors_combo.setGeometry(5, y, 320, 20)
        self.sectors_combo.addItems(
            ['Cardeais, colaterais e subcolaterais', 'Cardeais e colaterais', 'Cardeais']
        )
        self.sectors_combo.currentTextChanged.connect(self.sectors_changed)

        y += 25
        self.title_edit_label = QLabel('Título:', self)
        self.title_edit_label.setGeometry(5, y, 115, 18)

        y += 18
        self.title_edit = QLineEdit('Diagrama de roseta', self)
        self.title_edit.setGeometry(5, y, 320, 20)
        self.title_edit.textChanged.connect(self.title_changed)

        y+=30
        self.legend_checkbox = QCheckBox("Legenda:", self)
        self.legend_checkbox.setGeometry(5, y, 320, 18)
        self.legend_checkbox.clicked.connect(self.legend_checkbox_clicked)
        self.legend_checkbox.setEnabled(False)

        y+=18
        self.legend_title_edit = QLineEdit("Mergulho", self)
        self.legend_title_edit.setGeometry(5, y, 320, 20)
        self.legend_title_edit.textChanged.connect(self.legend_title_changed)
        self.legend_title_edit.setEnabled(False)

        y+=25
        self.column2_divisions_label = QLabel("Divisões de leque:", self)
        self.column2_divisions_label.setGeometry(5, y, 95, 20)
        self.column2_divisions_label.setEnabled(False)
        
        int_validator = QIntValidator(1, 100)

        self.column2_divisions_edit = QLineEdit("3", self)
        self.column2_divisions_edit.setGeometry(105, y, 30, 20)
        self.column2_divisions_edit.textChanged.connect(self.column2_divisions_changed)
        self.column2_divisions_edit.setEnabled(False)
        
        self.column2_interval_label = QLabel("Intervalo:", self)
        self.column2_interval_label.setGeometry(155, y, 60, 20)
        self.column2_interval_label.setEnabled(False)

        float_validator = QDoubleValidator(0, 9999, 3)
        float_validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        self.column2_min_edit = QLineEdit("0", self)
        self.column2_min_edit.setGeometry(210, y, 50, 20)
        self.column2_min_edit.setValidator(float_validator)
        self.column2_min_edit.textChanged.connect(lambda: self.column2_bound_changed(0))
        self.column2_min_edit.setEnabled(False)

        self.column2_interval_sep = QLabel("-", self)
        self.column2_interval_sep.setGeometry(260, y, 15, 20)
        self.column2_interval_sep.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.column2_max_edit = QLineEdit("90", self)
        self.column2_max_edit.setGeometry(275, y, 50, 20)
        self.column2_max_edit.setValidator(float_validator)
        self.column2_max_edit.textChanged.connect(lambda: self.column2_bound_changed(1))
        self.column2_max_edit.setEnabled(False)

        y += 30
        self.plot_diagram_button = QToolButton(self)
        self.plot_diagram_button.setText('Plotar diagrama')
        self.plot_diagram_button.setGeometry(5, y, 320, 30)
        self.plot_diagram_button.setEnabled(False)
        self.plot_diagram_button.clicked.connect(self.plot_diagram_button_pressed)

        y += 30
        self.copyright_label = QLabel(
            '© 2023 Gabriel Maccari <gabriel.maccari@hotmail.com>', self
        )
        self.copyright_label.setGeometry(5, y, 320, 20)
        self.copyright_label.setFont(QFont('Sans Serif', 8))

        y += 20
        self.setMinimumSize(330, y)
        self.setMaximumSize(330, y)

    def open_file_button_pressed(self):
        try:
            new_file_opened = False
            path = show_file_dialog(
                "Selecione uma tabela contendo os dados de entrada.",
                "Formatos suportados (*.xlsx *.xlsm *.csv *.ods);;",
                mode="open"
            )
            if path != "":
                new_file_opened = self.controller.read_file(path)
            if new_file_opened:
                self.column1_combo_label.setEnabled(True)
                self.column1_combo.setEnabled(True)
                self.column2_combo_checkbox.setEnabled(True)
                columns = self.controller.get_columns()
                self.fill_column_combos(columns)
                file_name = path.split("/")
                self.file_label.setText(file_name[-1])
        except Exception as exception:
            show_popup(f"ERRO: {exception}", msg_type="error")

    def fill_column_combos(self, columns):
        self.column1_combo.disconnect()
        self.column1_combo.clear()
        self.column1_combo.currentTextChanged.connect(lambda: self.column_selected(1))
        self.column1_combo.addItems(columns)

        self.column2_combo.disconnect()
        self.column2_combo.clear()
        self.column2_combo.currentTextChanged.connect(lambda: self.column_selected(2))
        self.column2_combo.addItems(columns)

    def column_selected(self, col: int):
        try:
            combobox = self.column1_combo if col == 1 else self.column2_combo
            selected_col = combobox.currentText()
            valid_col = self.controller.check_column(selected_col, col)

            if col == 1:
                self.column1_ok = valid_col
                val = self.column1_ok
            else:
                if self.column2_combo_checkbox.isChecked():
                    self.column2_ok = valid_col
                else:
                    self.column2_ok = True
                val = self.column2_ok

            check_icon = self.column1_check_icon if col == 1 else self.column2_check_icon
            icon = "icons/ok.png" if val else "icons/not_ok.png"
            tooltip = "OK" if val else "A coluna deve conter apenas dados numéricos entre 0 e 360"
            check_icon.setPixmap(QPixmap(icon).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
            check_icon.setToolTip(tooltip)

            if valid_col and col == 1:
                self.controller.column1 = selected_col
            elif valid_col and col == 2:
                self.controller.column2 = selected_col
                self.controller.set_column2_min_max()
                min_val = self.controller.column2_min_max[0]
                max_val = self.controller.column2_min_max[1]
                self.column2_min_edit.setText(f"{min_val}")
                self.column2_max_edit.setText(f"{max_val}")

            self.plot_diagram_button.setEnabled(self.column1_ok and self.column2_ok)
        except Exception as exception:
            show_popup(f"ERRO: {exception}", msg_type="error")

    def enable_column2_combo(self):
        try:
            enabled = self.column2_combo_checkbox.isChecked()
            self.column2_combo.setEnabled(enabled)
            self.column_selected(2)

            color = "#000000" if not enabled else "magma_r"
            self.color_button.setText(color)
            self.color_button.setStyleSheet(f"color: {color}")
            self.controller.bar_color = "#000000"
            self.color_button.disconnect()
            function = self.color_button_pressed if not enabled else self.colormap_button_pressed
            self.color_button.clicked.connect(function)

            self.legend_checkbox.setEnabled(enabled)
            if not enabled:
                self.legend_checkbox.setChecked(False)

            self.column2_divisions_label.setEnabled(enabled)
            self.column2_divisions_edit.setEnabled(enabled)
            self.column2_interval_label.setEnabled(enabled)
            self.column2_min_edit.setEnabled(enabled)
            self.column2_max_edit.setEnabled(enabled)

            if not enabled:
                self.controller.column2 = None
        except Exception as exception:
            show_popup(f"ERRO: {exception}", msg_type="error")

    def color_button_pressed(self):
        try:
            color = QColorDialog.getColor()
            color = color.name()
            self.controller.bar_color = color
            self.color_button.setStyleSheet(f"color: {color}")
            self.color_button.setText(color)
        except Exception as exception:
            show_popup(f"ERRO: {exception}", msg_type="error")

    def colormap_button_pressed(self):
        try:
            colormaps = matplotlib.pyplot.colormaps()
            colormap, ok = show_selection_dialog("Selecione o esquema de cores:", colormaps)
            if ok:
                self.controller.colormap = matplotlib.cm.get_cmap(colormap)
                self.color_button.setText(colormap)
        except Exception as exception:
            show_popup(f"ERRO: {exception}", msg_type="error")

    def title_changed(self):
        title = self.title_edit.text()
        self.controller.title = title

    def y_labels_position_changed(self):
        position = 90 - self.y_labels_position_spinbox.value()
        self.controller.y_labels_position = position

    def sectors_changed(self):
        sector_dict = {
            'Cardeais, colaterais e subcolaterais': 16,
            'Cardeais e colaterais': 8,
            'Cardeais': 4
        }
        sectors = sector_dict[self.sectors_combo.currentText()]
        self.controller.sectors = sectors

    def mirror_checkbox_clicked(self):
        self.controller.mirror_bars = self.mirror_checkbox.isChecked()

    def show_x_checkbox_clicked(self):
        self.controller.show_x_axis = self.x_axis_checkbox.isChecked()

    def show_x_labels_checkbox_clicked(self):
        self.controller.show_x_labels = self.x_labels_checkbox.isChecked()

    def show_y_checkbox_clicked(self):
        self.controller.show_y_axis = self.y_axis_checkbox.isChecked()

    def show_y_labels_checkbox_clicked(self):
        self.controller.show_y_labels = self.y_labels_checkbox.isChecked()

    def legend_checkbox_clicked(self):
        show_legend = self.legend_checkbox.isChecked()

        self.controller.show_legend = show_legend

        self.legend_title_edit.setEnabled(show_legend)
        self.legend_title_edit.setText("")
        
    def column2_divisions_changed(self):
        self.controller.bar_divisions = int(self.column2_divisions_edit.text())

    def column2_bound_changed(self, side: int):
        edit = self.column2_min_edit if side == 0 else self.column2_max_edit
        self.controller.column2_min_max[side] = float(edit.text())

    def legend_title_changed(self):
        self.controller.legend_title = self.legend_title_edit.text()

    def plot_diagram_button_pressed(self):
        try:
            matplotlib.pyplot.clf()
            fig = self.controller.plot_windrose()
            try:
                self.plot_window.close()
            except (UnboundLocalError, AttributeError):
                pass
            self.plot_window = PlotWindow(self, fig)
            self.plot_window.show()
        except Exception as exception:
            show_popup(f"ERRO: {exception.__class__} {exception}", msg_type="error")


class PlotWindow(QMainWindow):
    def __init__(self, parent, fig):
        super(PlotWindow, self).__init__(parent)

        self.parent = parent
        self.controller = parent.controller
        self.fig = fig

        self.folder = os.getcwd()

        img = self.get_plot_img()

        self.setWindowTitle("Plot results")
        self.setWindowIcon(QIcon('icons/windowIcon.ico'))

        image_icon = QIcon(img)
        self.plot_canvas = QPushButton(self)
        self.plot_canvas.setGeometry(0, 0, 450, 400)
        self.plot_canvas.setIcon(image_icon)
        self.plot_canvas.setIconSize(QSize(450, 400))
        self.plot_canvas.setFlat(True)

        self.image_path = QLabel(img, self)
        self.image_path.setGeometry(5, 380, 335, 15)
        self.image_path.setStyleSheet("font-size: 8pt; color: gray")

        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(395, 345, 50, 50)
        self.save_btn.setIcon(QIcon('icons/save.png'))
        self.save_btn.setIconSize(QSize(50, 50))
        self.save_btn.clicked.connect(self.save_plot)

        self.setMinimumWidth(450)
        self.setMaximumWidth(450)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)

    def get_plot_img(self):
        try:
            plot_folder = self.folder + '/plots'
            if not os.path.exists(plot_folder):
                os.makedirs(plot_folder)

            i = 0
            while True:
                fig_name = f"plots/plot{i}.png"
                if not os.path.exists(fig_name):
                    break
                i += 1

            matplotlib.pyplot.savefig(fig_name, dpi=300, transparent=True, format='png')
            return fig_name
        except Exception as e:
            show_popup(f"Não foi possível exibir o diagrama.\n\nMotivo: {e}", parent=self)
            self.close()

    def save_plot(self):
        try:
            output_file = show_file_dialog(
                "Salvar diagrama de roseta",
                "PNG (*.png);;JPEG (*.jpg);; SVG (*.svg)",
                "save"
            )
            if output_file != "":
                output_format = output_file[-3:]
                matplotlib.pyplot.savefig(
                    output_file,
                    dpi=300,
                    transparent=True,
                    format=output_format
                )
                show_popup("Arquivo salvo com sucesso!", parent=self)
        except Exception as e:
            show_popup(f"Não foi possível salvar o arquivo.\n\nMotivo: {e}", parent=self)

    def close_window(self):
        self.close()


def show_file_dialog(caption, extension_filter, mode="open", parent=None):
    dialog = QFileDialog(parent)
    if mode == "open":
        file_name, file_type = dialog.getOpenFileName(
            caption=caption, filter=extension_filter, parent=parent
        )
    else:
        file_name, file_type = dialog.getSaveFileName(
            caption=caption, filter=extension_filter, parent=parent
        )
    return file_name


def show_selection_dialog(message: str, items: list, selected=0,
                          title="Selecionar opções", parent=None):
    dialog = QInputDialog(parent)
    choice, ok = dialog.getItem(parent, title, message, items, selected,
                                      editable=False)
    return choice, ok


def show_wait_cursor(activate=True):
    if activate:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    else:
        QApplication.restoreOverrideCursor()


def show_popup(message, msg_type="notification", parent=None):
    popup_types = {
        "notification": {"title": "Notificação", "icon": "icons/info.png"},
        "error":        {"title": "Erro",        "icon": "icons/error.png"}
    }
    title = popup_types[msg_type]["title"]
    icon = QIcon(popup_types[msg_type]["icon"])

    popup = QMessageBox(parent)
    popup.setText(message)
    popup.setWindowTitle(title)
    popup.setWindowIcon(icon)
    popup.exec()
