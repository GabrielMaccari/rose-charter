# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 18:59:54 2022

@author: Gabriel Maccari
"""
import os
import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from windrose import WindroseAxes

def plot_windrose(values1: list[float], values2: list[float],
        number_of_sectors=16, number_of_divisions=6, title=None, bar_width=1,
        y_label_position=45, show_y=True, show_x=True, show_legend=True,
        legend_title='Legenda', legend_position='lower right',
        transparent_background=False, colors=cm.magma_r):
    """Função que plota um diagrama de roseta de duas variáveis (ex: Sentido de
    mergulho e mergulho de um plano; Direção e velocidade dos ventos; etc).

    PARÂMETROS
    -values1 (list[float]): Azimutes (floats entre 0 e 360);
    -values2 (list[float]): Mergulhos das estruturas ou velocidade dos ventos
    (floats);
    -number_of_sectors (integer): Número de setores direcionais no qual o
    diagrama ficará dividido (ex: 4 --> N, E, S e W). Default 16;
    -title (String): O título do diagrama;
    -bar_width (float): Largura das barras em relação à largura dos setores (0 a
     1). Default 1;
    -y_label_position (float): Posição dos rótulos das linhas da grade circular,
     em graus e em sentido anti-horário a partir do leste. Default = 45;
    -show_y (bool): Mostrar a grade circular. Default = True;
    -show_x (bool): Mostrar a grade radial. Default = True;
    -show_legend (bool): Mostrar a legenda. Default = True;
    -legend_title (String): Título da legenda (referente a values2). Default
    "Legenda";
    -legend_position (String): Posição da legenda do diagrama. Use "upper left",
     "upper right", "lower left" ou "lower right". Default "lower right";
    -transparent_background (bool): Se o fundo da imagem será transparente
    (True) ou branco (False). Default False;
    -colors (matplotlib colormap): O mapa de cores a ser utilizado no gráfico.
    Default cm.magma_r.

    RETORNA
    Nada.
    """

    if min(values1)<0 or max(values1)>360:
        raise Exception('A lista de azimutes informada contém valores fora do '
            'intervalo de 0-360°.')
    if number_of_sectors not in [4,8,16]:
        raise Exception('Número de setores do diagrama deve ser igual a 4, 8 ou'
                ' 16.')
    if bar_width<=0 or bar_width>1:
        raise Exception('A largura das barras deve ser um valor entre 0 e 1.')

    #Rótulos dos setores do diagrama
    label_dict = {
            4: ['E','N','W','S'],
            8: ['E','','N','','W','','S',''],
            16: ['E','','','','N','','','','W','','','','S','','','']
        }
    sector_labels = label_dict[number_of_sectors]

    #Calcula os setores e o ângulo de início com base no número de sentidos
    sector_width = 360 / number_of_sectors
    start_angle = (sector_width / 2) * (-1)
    sector_borders = numpy.arange(start_angle, 361+sector_width/2, sector_width)

    #Divisões das barras
    divisions = numpy.arange(0,90,(90/number_of_divisions))

    #Por causa de algum bug estranho, se você plota um histograma aleatório
    # antes de plotar o diagrama de roseta, ele arredonda os finais das barras e
    # fica mais bonito
    plt.hist([0, 1])
    plt.close()

    #Cria a figura
    fig = plt.figure(figsize=(8,8), dpi=300)
    ax = WindroseAxes.from_ax()
    ax.bar(values1, values2, normed=False, nsector=number_of_sectors,
            opening=bar_width, edgecolor='white', cmap=colors, bins=divisions)

    #Ajusta o diagrama
    ax.set_thetagrids(numpy.arange(0, 360, sector_width), labels=sector_labels)
    ax.set_facecolor('white')
    ax.set_rlabel_position(y_label_position)
    if title: ax.set_title(title, y=1.07, fontsize=18, fontweight='bold')
    if show_y: ax.yaxis.grid(True)
    if show_x: ax.xaxis.grid(True)
    if show_legend: ax.set_legend(title=legend_title, loc='lower right')

    return fig


def plot_polar_histogram(values: list[float], number_of_sectors=16,
        number_of_yticks=4, mirror=False, title=None, color='black',
        bar_width=1, y_label_position=45, show_y=True,
        show_x=True, transparent_background=False):

    """Função que plota um histograma polar de direções (diagrama de roseta).

    PARÂMETROS
    -values (list[float]): Azimutes (floats entre 0 e 360);
    -number_of_sectors (integer): Número de setores direcionais no qual o
    diagrama ficará dividido (ex: 4 --> N, E, S e W). Default 16;
    -mirror (bool): Soma as contagens de direções opostas e as duplica, plotando
    um diagrama espelhado. Default False;
    -title (String): O título do diagrama;
    -color (String): Cor das barras do histograma. Default 'black'.
    -bar_width (float): Largura das barras em relação à largura dos setores (0 a
     1). Default 1;
    -y_label_position (float): Posição dos rótulos das linhas da grade circular,
     em graus e em sentido horário a partir do norte. Default = 45;
    -show_y (bool): Mostrar a grade circular. Default = True;
    -show_x (bool): Mostrar a grade radial. Default = True;
    -transparent_background (bool): Se o fundo da imagem será transparente
    (True) ou branco (False). Default False;

    RETORNA
    Nada.
    """

    if min(values)<0 or max(values)>360:
        raise Exception('A lista de azimutes informada contém valores fora do '
            'intervalo de 0-360°.')
    if number_of_sectors not in [4,8,16]:
        raise Exception('Número de setores do diagrama deve ser igual a 4, 8 ou'
                ' 16.')
    if bar_width<=0 or bar_width>1:
        raise Exception('A largura das barras deve ser um valor entre 0 e 1.')

    #Rótulos dos setores do diagrama
    label_dict = {
            4: ['E','N','W','S'],
            8: ['E','','N','','W','','S',''],
            16: ['E','','','','N','','','','W','','','','S','','','']
        }
    sector_labels = label_dict[number_of_sectors]

    #Calcula os setores e o ângulo de início com base no número de sentidos
    sector_width = 360 / number_of_sectors
    start_angle = (sector_width / 2) * (-1)
    sector_borders = numpy.arange(start_angle, 361+sector_width/2, sector_width)

    #Calcula a largura das barras
    bar_width = sector_width * bar_width

    # Realiza a contagem de valores em cada um dos setores
    count, sector_borders = numpy.histogram(values, sector_borders)
    # Soma a primeira e a última contagem (ambas são N)
    count[0] += count[-1]

    #Cria e configura o diagrama
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_subplot(111, projection='polar')

    #Plota os valores do histograma
    if mirror == True:
        # Divide os dados em dois conjuntos (0-180 e 180-360), soma os dois e
        # duplica
        half = numpy.sum(numpy.split(count[:-1], 2), 0)
        two_halves = numpy.concatenate([half, half])
        #Plota
        ax.bar(numpy.deg2rad(numpy.arange(0, 360, sector_width)), two_halves,
                width=numpy.deg2rad(bar_width), edgecolor='white', color=color,
                bottom=0.0)
    else:
        #Plota
        ax.bar(numpy.deg2rad(numpy.arange(0, 360, sector_width)), count[:-1],
               width=numpy.deg2rad(bar_width), edgecolor='white', color=color,
               bottom=0.0)

    #Ajusta o gráfico
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(numpy.arange(0, 360, sector_width), labels=sector_labels)
    ax.set_rlabel_position(y_label_position)
    if title: ax.set_title(title, y=1.10, fontsize=18, fontweight='bold')
    ax.yaxis.grid(show_y)
    ax.xaxis.grid(show_x)

    return fig


def main():
    folder = os.getcwd()
    #Tabela e colunas dos dados de entrada
    data = pandas.read_excel(f'{folder}\\exemplo_dados_entrada.xlsx',
            sheet_name=0, engine='openpyxl')
    field1 = 'sentido_de_mergulho'
    field2 = 'mergulho'

    #Extrai os dados da tabela
    values1 = data[field1].dropna().values
    values2 = data[field2].dropna().values

    fig1 = plot_polar_histogram(values1)
    plt.savefig('polar_histogram.png', dpi=300)

    plt.clf()

    fig2 = plot_windrose(values1, values2)
    plt.savefig('windrose.png', dpi=300)

    print('Done!')


if __name__ == '__main__':
    main()
