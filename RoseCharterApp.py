# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 16:02:14 2022

@author: Gabriel Maccari
"""

from sys import argv as sys_argv
from os import getcwd
import pandas
import numpy
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QCheckBox, QLineEdit, QColorDialog, QFileDialog, QFrame, QMessageBox, QDoubleSpinBox, QInputDialog
from PyQt6.QtGui import QIcon, QFont
from PlotWindow import PlotWindow

class RoseCharterApp(QMainWindow):
    def __init__(self):
        
        self.folder = getcwd()
        self.fileOpened = False
        self.column = None
        self.mirror = False
        self.selectColor = False
        self.color = 'black'
        self.title = 'Diagrama de roseta'
        self.fileOut = 'diagrama.png'
        self.show_xAxis = True
        self.show_yAxis = True
        self.show_xLabels = True
        self.show_yLabels = True
        self.rLabel_position = 33.75
        self.chart_directions = 'Cardeais, colaterais e subcolaterais'
        
        super().__init__()
        self.setWindowTitle('Rose Charter')
        self.setWindowIcon(QIcon('icons/windowIcon.ico'))
        
        y=5
        self.filePromptLabel = QLabel('Selecione um arquivo .xlsx contendo os dados.', self)
        self.filePromptLabel.setGeometry(5, y, 260, 25)

        self.fileButton = QPushButton('Selecionar', self)
        self.fileButton.setGeometry(265, y, 80, 25)
        self.fileButton.clicked.connect(self.open_file)
        
        y+=30
        self.line1 = QFrame(self)
        self.line1.setGeometry(5, y, 340, 3)
        self.line1.setLineWidth(1)
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFrameShadow(QFrame.Shadow.Sunken)
        
        y+=10
        self.columnPromptLabel = QLabel('Coluna dos dados de direção ou sentido (0-360):', self)
        self.columnPromptLabel.setGeometry(5, y, 340, 20)
        
        y+=20
        self.columnCombo = QComboBox(self)
        self.columnCombo.setGeometry(5, y, 340, 25)
        self.columnCombo.setEnabled(False)
        self.columnCombo.currentTextChanged.connect(self.select_column)
        
        y+=30
        self.columnVerifyLabel = QLabel('', self)
        self.columnVerifyLabel.setGeometry(5, y, 340, 20)
        
        y+=25
        self.line2 = QFrame(self)
        self.line2.setGeometry(5, y, 340, 3)
        self.line2.setLineWidth(1)
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)
        
        y+=10
        self.settingsLabel = QLabel('Configurações:', self)
        self.settingsLabel.setGeometry(5, y, 340, 20)
        
        y+=25
        self.mirrorCheckBox = QCheckBox('Espelhar dados', self)
        self.mirrorCheckBox.setGeometry(5, y, 170, 20)
        self.mirrorCheckBox.setToolTip('Ao selecionar esta opção, sentidos opostos (ex: E e W) serão somados e espelhados.')
        self.mirrorCheckBox.stateChanged.connect(self.check_mirror)
        self.mirrorCheckBox.setEnabled(False)
        
        self.xAxisCheckBox = QCheckBox('Esconder eixo X', self)
        self.xAxisCheckBox.setGeometry(170, y, 170, 20)
        self.xAxisCheckBox.stateChanged.connect(self.check_hideX)
        self.xAxisCheckBox.setEnabled(False)
        
        y+=20
        self.colorCheckBox = QCheckBox('Cor das barras:', self)
        self.colorCheckBox.setGeometry(5, y, 100, 20)
        self.colorCheckBox.stateChanged.connect(self.check_colorSelect)
        self.colorCheckBox.setEnabled(False)
        
        self.colorButton = QPushButton('#000000', self)
        self.colorButton.setGeometry(105, y, 55, 20)
        self.colorButton.clicked.connect(self.color_select)
        self.colorButton.setEnabled(False)
        
        self.yAxisCheckBox = QCheckBox('Esconder eixo Y', self)
        self.yAxisCheckBox.setGeometry(170, y, 170, 20)
        self.yAxisCheckBox.stateChanged.connect(self.check_hideY)
        self.yAxisCheckBox.setEnabled(False)
        
        y+=20
        self.xLabelCheckBox = QCheckBox('Esconder rótulos de X', self)
        self.xLabelCheckBox.setGeometry(5, y, 170, 20)
        self.xLabelCheckBox.stateChanged.connect(self.check_hideXLabels)
        self.xLabelCheckBox.setEnabled(False)
        
        self.yLabelCheckBox = QCheckBox('Esconder rótulos de Y', self)
        self.yLabelCheckBox.setGeometry(170, y, 170, 20)
        self.yLabelCheckBox.stateChanged.connect(self.check_hideYLabels)
        self.yLabelCheckBox.setEnabled(False)
        
        y+=25
        self.rLabelPositionLabel = QLabel('Posição dos rótulos de Y (°):', self)
        self.rLabelPositionLabel.setGeometry(5, y, 150, 20)
        self.rLabelPositionLabel.setEnabled(False)
        
        self.rLabelPositionSpin = QDoubleSpinBox(self)
        self.rLabelPositionSpin.setGeometry(155, y, 55, 20)
        self.rLabelPositionSpin.setRange(0, 360)
        self.rLabelPositionSpin.setValue(33.75)
        self.rLabelPositionSpin.setEnabled(False)
        
        y+=25
        self.directionsLabel = QLabel('Direções:', self)
        self.directionsLabel.setGeometry(5, y, 160, 20)
        
        y+=20
        self.directionsCombo = QComboBox(self)
        self.directionsCombo.setGeometry(5, y, 340, 23)
        self.directionsCombo.addItems(['Cardeais, colaterais e subcolaterais', 'Cardeais e colaterais', 'Cardeais'])
        self.directionsCombo.setEnabled(False)
        
        y+=28
        self.titlePromptLabel = QLabel('Título do diagrama:', self)
        self.titlePromptLabel.setGeometry(5, y, 115, 20)
        
        y+=20
        self.titleEdit = QLineEdit('Diagrama de roseta', self)
        self.titleEdit.setGeometry(5, y, 340, 22)
        self.titleEdit.setEnabled(False)
        
        y+=25
        self.buildChartButton = QPushButton('Construir diagrama', self)
        self.buildChartButton.setGeometry(5, y, 340, 30)
        self.buildChartButton.setEnabled(False)
        self.buildChartButton.clicked.connect(self.build_diagram)
        
        y+=30
        self.copyrightLabel = QLabel('© 2022 Gabriel Maccari <gabriel.maccari@hotmail.com>', self)
        self.copyrightLabel.setGeometry(5, y, 340, 20)
        self.copyrightLabel.setFont(QFont('Sans Serif', 8))
        
        y+=20
        self.setMinimumSize(350, y)
        self.setMaximumSize(350, y)
       
    def enable_widgets(self, col_state, state):
        self.columnCombo.setEnabled(col_state)
        self.mirrorCheckBox.setEnabled(state)
        self.colorCheckBox.setEnabled(state)
        if self.colorCheckBox.isEnabled() and self.colorCheckBox.isChecked():
            self.colorButton.setEnabled(True)
        else:
            self.colorButton.setEnabled(False)
        self.xAxisCheckBox.setEnabled(state)
        self.yAxisCheckBox.setEnabled(state)
        self.xLabelCheckBox.setEnabled(state)
        self.yLabelCheckBox.setEnabled(state)
        self.directionsCombo.setEnabled(state)
        self.titleEdit.setEnabled(state)
        self.buildChartButton.setEnabled(state)
        self.rLabelPositionLabel.setEnabled(state)
        self.rLabelPositionSpin.setEnabled(state)
       
    def open_file(self):
        self.fileOpened = False
        #Abre um diálogo para seleção do arquivo. Os formatos suportados são xlsx, xlsm, csv e ods
        try:
            inFile = QFileDialog.getOpenFileName(self, caption='Selecione uma tabela contendo os dados de entrada.', directory=self.folder, filter='Formatos suportados (*.xlsx *.xlsm *.csv *.ods);;Pasta de Trabalho do Excel (*.xlsx);;Pasta de Trabalho Habilitada para Macro do Excel (*.xlsm);;CSV (*.csv);; OpenDocument Spreadsheet (*.ods)')
        #Se não der para abrir o arquivo, mostra uma mensagem com o erro
        except Exception as e:
            msg = QMessageBox(parent=self, text='Não foi possível abrir o arquivo selecionado.\n\nERRO: %s' % (str(e)))
            msg.setWindowTitle('Erro')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
        
        path = inFile[0]
        
        #Se algum arquivo tiver sido selecionado com sucesso
        if path != '':
            try:
                #Cria um dataframe a partir de um arquivo csv
                if path.endswith('.csv'):
                    file = pandas.read_csv(path, decimal=',', delimiter=';')
                    self.fileOpened = True
                #Cria um dataframe a partir de um arquivo xlsx, xlsm ou ods
                else:
                    #Engine odf para arquivos ods e openpyxl para arquivos do excel
                    eng=('odf' if path.endswith('.ods') else 'openpyxl')
                    wholeFile = pandas.ExcelFile(path, engine=eng)
                    sheetNames = wholeFile.sheet_names
                    #Caso o arquivo tenha mais de uma planilha, mostra um diálogo com uma comboBox para selecionar a planilha dos dados
                    if len(sheetNames) > 1:
                        sheet, ok = QInputDialog.getItem(self, 'Selecionar aba', 'Planilha:', sheetNames)
                        #Se o usuário apertar ok no diálogo, cria o dataframe a partir da planilha selecionada
                        if ok:
                            file = wholeFile.parse(sheet_name=sheet)
                        #Caso o usuário aperte em cancelar ou fechar o diálogo, cancela a leitura do arquivo
                        else:
                            return
                    #Se o arquivo tiver apenas uma planilha, cria o dataframe com ela
                    else:
                        file = pandas.read_excel(path, engine=eng)
                    
                    #Remove colunas e linhas em branco
                    remove_cols = [col for col in file.columns if 'Unnamed' in col]
                    file.drop(remove_cols, axis='columns', inplace=True)
                    file.replace(r'^\s*$', numpy.nan, inplace=True, regex=True)
                    file.dropna(how='all', axis='index', inplace=True)
                    
                    self.fileOpened = True
                    
            #Caso ocorra algum erro na leitura do arquivo, exibe uma mensagem com o erro e esvazia as combo boxes
            except Exception as e:
                self.fileOpened = False
                msg = QMessageBox(parent=self, text='Não foi possível abrir o arquivo.\n\n'+str(e))
                msg.setWindowTitle('Erro')
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()
                self.pitchColumn_cmb.clear()
                self.filePromptLabel.setText('Não foi possível abrir o arquivo.')
                self.filePromptLabel.setStyleSheet('QLabel {color: red}')
        else:
            return
                
        if self.fileOpened:
            self.df = file
            self.filePromptLabel.setText('Arquivo carregado com sucesso.')
            self.filePromptLabel.setStyleSheet('QLabel {color: green}')
            self.columnCombo.clear()
            self.columnCombo.setEnabled(True)
            self.columnCombo.addItems(self.df.columns.to_list())
        else:
            self.filePromptLabel.setText('Não foi possível abrir o arquivo.')
            self.filePromptLabel.setStyleSheet('QLabel {color: red}')
            self.columnCombo.clear()
            self.enable_widgets(False, False)
    
    def select_column(self, col):
        try:
            self.df[col] = self.df[col].astype(float)
            if self.df[col].dropna().between(0,360).all():
                self.column = col
                self.columnVerifyLabel.setText('OK! A coluna selecionada contém apenas dados numéricos.')
                self.columnVerifyLabel.setStyleSheet('QLabel {color: green}')
                self.enable_widgets(True, True)
            else:
                self.columnVerifyLabel.setText('ATENÇÃO! Dados fora do intervalo permitido (0-360).')
                self.columnVerifyLabel.setStyleSheet('QLabel {color: red}')
                self.enable_widgets(True, False)
        except:
            self.columnVerifyLabel.setText('ATENÇÃO! A coluna selecionada contém dados não-numéricos.')
            self.columnVerifyLabel.setStyleSheet('QLabel {color: red}')
            self.column_OK = False
            self.enable_widgets(True, False)
    
    def check_mirror(self):
        self.mirror = not self.mirror
    
    def check_colorSelect(self):
        self.selectColor = not self.selectColor
        self.colorButton.setEnabled(self.selectColor)
        if self.selectColor == False:
            self.color = '#000000'
            self.colorButton.setText(self.color)
            self.colorButton.setStyleSheet("color: %s" % (self.color))
    
    def color_select(self):
        color = QColorDialog.getColor()
        self.color = color.name()
        self.colorButton.setStyleSheet("color: %s" % (self.color))
        self.colorButton.setText(self.color)
    
    def check_hideX(self):
        self.show_xAxis = not self.show_xAxis
    
    def check_hideY(self):
        self.show_yAxis = not self.show_yAxis
    
    def check_hideYLabels(self):
        self.show_yLabels = not self.show_yLabels
        self.rLabelPositionLabel.setEnabled(self.show_yLabels)
        self.rLabelPositionSpin.setEnabled(self.show_yLabels)
    
    def check_hideXLabels(self):
        self.show_xLabels = not self.show_xLabels
        
    def build_diagram(self):
        
        try:
        
            self.chart_directions = self.directionsCombo.currentText()
            self.title = self.titleEdit.text()
            if not self.colorCheckBox.isChecked(): self.color = 'black'
            
            self.rLabel_position = self.rLabelPositionSpin.value()
            
            direcoes = self.df[self.column].values
            
            if self.chart_directions == 'Cardeais, colaterais e subcolaterais':
                angle_start = -11.25
                angle_interval = 22.5
                bar_width = 20
                if self.show_xLabels==True:
                    labels = ['N','','','','E','','','','S','','','','W','','','']
                else:
                    labels = ['','','','','','','','','','','','','','','','']
            elif self.chart_directions == 'Cardeais e colaterais':
                angle_start = -22.5
                angle_interval = 45
                bar_width = 42.5
                if self.show_xLabels==True:
                    labels = ['N','','E','','S','','W','']
                else:
                    labels = ['','','','','','','','']
            elif self.chart_directions == 'Cardeais':
                angle_start = -45
                angle_interval = 90
                bar_width = 87.5
                if self.show_xLabels==True:
                    labels = ['N','E','S','W']
                else:
                    labels = ['','','','']
            
            #Cria 16 divisões de 22.5 graus para os pontos cardeais, colaterais e subcolaterais
            bin_edges = numpy.arange(angle_start, 361, angle_interval)
            
            #Realiza a contagem de valores em cada uma das direções a partir das divisões criadas
            number_of_strikes, bin_edges = numpy.histogram(direcoes, bin_edges)
            #Soma a primeira e a última contagem (ambas são N)
            number_of_strikes[0] += number_of_strikes[-1]
            
            fig = plt.figure(figsize=(8,8), dpi=300)
    
            ax = fig.add_subplot(111, projection='polar')
    
            if self.mirror == True:
                #Divide os dados em dois conjuntos (0-180 e 180-360), soma os dois e duplica
                half = numpy.sum(numpy.split(number_of_strikes, 2), 0)
                two_halves = numpy.concatenate([half, half])
                ax.bar(numpy.deg2rad(numpy.arange(0, 360, angle_interval)), two_halves, width=numpy.deg2rad(bar_width), bottom=0.0, edgecolor='white', color=self.color)
            else:
                ax.bar(numpy.deg2rad(numpy.arange(0, 360, angle_interval)), number_of_strikes, width=numpy.deg2rad(bar_width), bottom=0.0, edgecolor='white', color=self.color)
                
            ax.set_facecolor('white')
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_thetagrids(numpy.arange(0, 360, angle_interval), labels=labels)
            ax.set_rlabel_position(self.rLabel_position)
            
            if self.title != '':
                ax.set_title(self.title, y=1.10, fontsize=18, fontweight='bold')
            
            if self.show_yLabels==False:
                ax.yaxis.set_ticklabels([])
                
            ax.yaxis.grid(self.show_yAxis)
            ax.xaxis.grid(self.show_xAxis)

        except Exception as e:
            msg = QMessageBox(parent=self, text='Não foi possível gerar o diagrama.\n\n'+str(e))
            msg.setWindowTitle("Erro")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
        
        #plt.show()
        
        self.plotWindow = PlotWindow(plt, self)
        self.plotWindow.show()

if __name__ == '__main__':
    app = QApplication(sys_argv)
    window = RoseCharterApp()
    window.show()
    app.exec()