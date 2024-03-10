import plotly.express as px
import numpy as np
import pandas as pd

def print_graph_bar(df):
    #z = df.drop(['datetime'], axis=1)
    col_list = list(df.columns)
    col_list.remove('datetime')

    #df['sums'] = df[col_list].sum(axis=1)
    dddf = df.copy(deep=True)
    dddf['sums'] = dddf[col_list].sum(axis=1)
    dddf['cumsums'] = dddf['sums'].cumsum()
    fig = px.bar(dddf,x='datetime',y='cumsums',title='Сумма накоплений за весь период от всех представленных облигаций')
    fig.update_traces(marker_color='green')
    fig.update_layout(plot_bgcolor='violet')
    return fig


#df = pd.read_excel('/home/nikolas/OTUSHeadProject/.venv/matrixbonds2.xlsx')
#g_data = df[(df['datetime'] > '2015-06-24 00:00:00+00:00') & (df['datetime'] < '2031-04-28 00:00:00+00:00')]
#figgg = print_graph_bar(g_data)
#figgg.show()

def print_month_bar(df,val_bond):
    dates = df['datetime']                #Получаем колонку дат
    bonds = df.columns.tolist()[1:]  # Получаем колонки облигаций (bonds) без первой колонки (даты в ней).

    z = df.drop(['datetime'],axis=1).to_numpy()  # Получаем данные выплат без первой колонки и преобразуем в numpy массив
    mask1 = (z == 0.0).all(0)  # Ищем маску тех колонок где одни только нули
    column_indices = np.where(mask1)[0]  # По полученной маске определяем номмера колонок с нулями
    z = z[:, ~mask1]  # Удаляем те колонки из списка mask1
    new_bonds = []
    for i in range(len(bonds)):
        if i not in column_indices:
            new_bonds.append(bonds[i])

    col_list = new_bonds[val_bond[0]:val_bond[1]]  # Создаем список названий колонок выбрав те которые в RangeSlider
    z = z[:, val_bond[0]:val_bond[1]]  # Выделяем те, которые хотим с помощью RangeSlider

    glue_df = pd.DataFrame(data=z,index=dates,columns=col_list)

    dddg = glue_df.copy(deep=True)
    #dddg['sums'] = dddg['sums'].cumsum()
    dddg['sums'] = dddg[col_list].sum(axis=1)
    dddg['cumsums'] = dddg['sums'].cumsum()
    fig = px.bar(dddg,x=dddg.index,y='cumsums',title='Сумма накоплений за месяц от всех представленных облигаций')
    fig.update_traces(marker_color='green')
    fig.update_layout(plot_bgcolor='violet')

    return fig