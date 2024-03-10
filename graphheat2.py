#import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def print_heat_map(df):
    dates = df['datetime']                #Получаем колонку дат
    bonds = df.columns.tolist()[1:]       #Получаем колонки облигаций (bonds) без первой колонки (даты в ней).
    z = df.drop(['datetime'], axis=1).to_numpy()  #Получаем данные выплат без первой колонки и преобразуем в numpy массив
    z = np.where(z > 0, 1, 0)             #Заменим выплаты на 1 - есть выплата и 0 - нет выплат
    fig = go.Figure(data=go.Heatmap(z=z, x=bonds, y=dates, colorscale='Viridis'))
    fig.update_yaxes(autorange="reversed")   #Перевернем даты в направление вниз. Так как таблица растет вниз и вправо
    fig.update_layout(
        title='Общий календарь купонных выплат. Здесь отображено только наличие выплаты. Размер не учитывается.')
    return fig

def print_month_heat(df,val_bond):
    dates = df['datetime']                #Получаем колонку дат
    bonds = df.columns.tolist()[1:]       #Получаем колонки облигаций (bonds) без первой колонки (даты в ней).


    z = df.drop(['datetime'], axis=1).to_numpy()  #Получаем данные выплат без первой колонки и преобразуем в numpy массив
    mask1 = (z == 0.0).all(0)  #Ищем маску тех колонок где одни только нули

    column_indices = np.where(mask1)[0]    #По полученной маске определяем номмера колонок с нулями

    z = z[:, ~mask1]           #Удаляем те колонки из списка mask1

    new_bonds = []
    for i in range(len(bonds)):
        if i not in column_indices:
            new_bonds.append(bonds[i])

    col_list = new_bonds[val_bond[0]:val_bond[1]]  # Создаем список названий колонок выбрав те которые в RangeSlider
    z = z[:, val_bond[0]:val_bond[1]]             #Выделяем те, которые хотим с помощью RangeSlider
    #X = data[:, [1, 9]]
    #z = np.where(z > 0, 1, 0)             #Заменим выплаты на 1 - есть выплата и 0 - нет выплат
    fig = go.Figure(data=go.Heatmap(z=z, x=col_list, y=dates, colorscale='oranges'))
    fig.update_yaxes(autorange="reversed")   #Перевернем даты в направление вниз. Так как таблица растет вниз и вправо
    fig.update_layout(
        title='Календарь купонных выплат за выбранный период. Здесь отображена также величина выплаты.')
    return fig