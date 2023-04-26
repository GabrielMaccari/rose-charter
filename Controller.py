import pandas
import numpy
import matplotlib
import matplotlib.pyplot as plt
from csv import Sniffer
from windrose import WindroseAxes

from View import show_selection_dialog, show_wait_cursor

matplotlib.use("svg")


class Controller:
    def __init__(self):
        self.df = None
        self.column1 = None
        self.column2 = None
        self.mirror_bars = False
        self.show_x_axis = True
        self.show_x_labels = True
        self.show_y_axis = True
        self.show_y_labels = True
        self.bar_color = "#000000"
        self.y_labels_position = 33.75
        self.sectors = 16
        self.title = ""
        self.colormap = matplotlib.cm.magma_r
        self.show_legend = True
        self.legend_position = "lower right"
        self.legend_title = ""
        self.bar_divisions = 3
        self.column2_min_max = [0, 90]

    def read_file(self, path):
        show_wait_cursor()
        # Arquivo csv
        if path.endswith(".csv"):
            sniffer = Sniffer()
            data = open(path, "r").read(4096)
            sep = str(sniffer.sniff(data).delimiter)
            df = pandas.read_csv(path, delimiter=sep)
        # Arquivo xlsx, xlsm ou ods
        else:
            engine = ("odf" if path.endswith(".ods") else "openpyxl")
            excel_file = pandas.ExcelFile(path, engine=engine)
            sheets = excel_file.sheet_names
            # Se houver mais de 1 aba, o usuário seleciona uma delas
            if len(sheets) > 1:
                multiple_sheets = True
                show_wait_cursor(False)
                sheet, ok = show_selection_dialog(
                    "Selecione a aba desejada:", sheets
                )
                show_wait_cursor()
                if not ok:
                    show_wait_cursor(False)
                    return False
            else:
                sheet = 0
            df = excel_file.parse(sheet_name=sheet)
        show_wait_cursor(False)
        # Checa se o dataframe foi criado ou não
        if isinstance(df, pandas.DataFrame):
            self.df = df.copy()
            return True
        else:
            return False

    def get_columns(self):
        return self.df.columns.to_list()

    def check_column(self, selected_column, col=1):
        df = self.df
        try:
            df[selected_column] = df[selected_column].replace(",", ".", regex=True)
            df[selected_column] = df[selected_column].astype("float64")

            if col == 1:
                if not df[selected_column].dropna().between(0, 360).all():
                    return False

            self.df[selected_column] = df[selected_column]
            return True
        except ValueError:
            return False

    def set_column2_min_max(self):
        values = self.df[self.column2].dropna().values
        min_val = min(values)
        max_val = max(values)
        self.column2_min_max = [min_val, max_val]

    def plot_windrose(self):

        values1 = self.df[self.column1]

        # Rótulos dos setores do diagrama
        x_label_dict = {
            4: ['E', 'N', 'W', 'S'],
            8: ['E', '', 'N', '', 'W', '', 'S', ''],
            16: ['E', '', '', '', 'N', '', '', '', 'W', '', '', '', 'S', '', '', '']
        }
        x_labels = x_label_dict[self.sectors]
        if not self.show_x_labels:
            for i, item in enumerate(x_labels):
                x_labels[i] = ""

        # Calcula os setores e o ângulo de início com base no número de sentidos
        sector_width = 360 / self.sectors
        start_angle = (sector_width / 2) * (-1)
        sector_borders = numpy.arange(start_angle, 361 + sector_width / 2, sector_width)

        # Divisões das barras
        divisions = None
        if self.column2 is not None:
            values2 = self.df[self.column2]
            min_val, max_val = self.column2_min_max[0], self.column2_min_max[1]
            divisions = numpy.arange(min_val, max_val, (max_val/self.bar_divisions))
        else:
            values2 = [1 for x, val in enumerate(values1)]
            divisions = numpy.arange(0, 1, 1)

        # Espelha os dados
        if self.mirror_bars:
            mirrored_values = []
            for v in values1:
                mirrored_values.append(v + 180 if v < 180 else v - 180)
            values1_mirror = numpy.array(mirrored_values)
            values1 = numpy.concatenate((values1, values1_mirror))
            values2 = numpy.concatenate((values2, values2))

        # Por causa de algum bug estranho, se você plota um histograma aleatório
        # antes de plotar o diagrama de roseta, ele arredonda os finais das
        # barras e fica mais bonito
        plt.hist([0, 1])

        # Cria a figura
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = WindroseAxes.from_ax()
        if self.column2 is not None:
            ax.bar(values1, values2, normed=False, nsector=self.sectors,
                   opening=1, cmap=self.colormap, edgecolor='white',
                   bins=divisions)
            if self.show_legend:
                ax.set_legend(title=self.legend_title, loc=self.legend_position)
        else:
            ax.bar(values1, values2, normed=False, nsector=self.sectors,
                   opening=1, colors=self.bar_color, edgecolor='white',
                   bins=divisions)

        # Ajusta o diagrama
        ax.set_thetagrids(numpy.arange(0, 360, sector_width), labels=x_labels)
        ax.set_facecolor('white')
        ax.set_rlabel_position(self.y_labels_position)
        if not self.show_y_labels:
            ax.yaxis.set_ticklabels([])
        if self.title != "":
            ax.set_title(self.title, y=1.07, fontsize=18, fontweight='bold')

        ax.yaxis.grid(self.show_y_axis)
        ax.xaxis.grid(self.show_x_axis)

        return fig

