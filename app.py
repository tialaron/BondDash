#Импорт
from dash import Dash, dcc,html,Input,Output,State, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import date

from graphheat2 import print_heat_map, print_month_heat
from graph_bar01 import print_graph_bar, print_month_bar


#Данные и приложение
df = pd.read_excel('H:\\Pythonprojects\\OTUSHeadProject02\\venv\\matrixbonds2.xlsx')
df['datetime'] = pd.to_datetime(df['datetime'])
min_date = (df['datetime'].min())
max_date = (df['datetime'].max())

date_shape = df.shape
bonds_numb = df.shape[1]-1
app = Dash(__name__,external_stylesheets=[dbc.themes.SOLAR])
#Элементы
datepickerrange = dcc.DatePickerRange( id='date_range', display_format='DD-MM-YYYY',  min_date_allowed=min_date, max_date_allowed=max_date, start_date=min_date,
    end_date=max_date)

monthpickerrange = dcc.DatePickerRange(id='month_range', display_format='DD-MM-YYYY', min_date_allowed=min_date, max_date_allowed=max_date,start_date=min_date,
                                       end_date=max_date)
month_rangeslider = dcc.RangeSlider(id='month_slider',min=0,max=bonds_numb,step=1,value=[0,bonds_numb])

month_date_picker = dcc.DatePickerSingle(id='date_picker', display_format='DD-MM-YYYY',min_date_allowed=min_date,max_date_allowed=max_date,date=date(2017, 8, 25))
#Макетирование
app.layout = dbc.Container(
    html.Div([
        #Header
        html.Div([html.H1("Прогноз доходности облигаций",className="zagolovok")]),
        #Body

    #dbc.Container(
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Доход от всех облигаций',children=[
                    html.Div([
                        dbc.Row([
                            dbc.Col(html.H4(f"Всего в таблице {date_shape[0]} строк и {date_shape[1]-1} облигаций ")),
                            dbc.Col(datepickerrange)
                            ])
                        ]),
                    html.Div([
                        dcc.Graph(id="heat_map",figure=print_heat_map(df=df)),
                        dcc.Graph(id="bond_bar",figure=print_graph_bar(df=df))
                        ])
                    ]),
                dcc.Tab(label='Доход от выбранных облигаций за месяц',children=[
                    html.Div([
                        dbc.Row([
                            dbc.Col(month_rangeslider),
                            dbc.Col(monthpickerrange)
                        ])
                    ]),
                    html.Div([
                        dcc.Graph(id="month_heat"),
                        dcc.Graph(id="month_bar")
                    ])

                ])
            ])

            ]),

        #Footer
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(html.H3('OTUS. Курс Bi-аналитика')),align='center'),
                dbc.Col(html.P("Лисин Николай, 2023 г."),align='center')
                ],align='center')
            ])
        ])
)


#Callback
@app.callback(
    Output(component_id='heat_map',component_property='figure'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date')
)
def heatmap_filter(start_date,end_date):
    f_data = df.copy(deep=True)
    f_data = f_data[(f_data['datetime'] > start_date) & (f_data['datetime'] < end_date)]
     #if bool(value)  is not None:
     #    f_data = f_data[f_data['Channel'].isin(value)].copy(deep=True)
    return print_heat_map(df=f_data)

@app.callback(
    Output(component_id='bond_bar',component_property='figure'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date')
)
def bond_filter(start_date,end_date):
    g_data = df.copy(deep=True)
    g_data = g_data[(g_data['datetime'] > start_date) & (g_data['datetime'] < end_date)]
    return print_graph_bar(df=g_data)

@app.callback(
    Output(component_id='month_heat',component_property='figure'),
    Input(component_id='month_range',component_property='start_date'),
    Input(component_id='month_range',component_property='end_date'),
    Input(component_id='month_slider',component_property='value')
)
def month_heatmap_source(start_date,end_date,value):
    b_data = df.copy(deep=True)
    b_data = b_data[(b_data['datetime'] > start_date) & (b_data['datetime'] < end_date)]
    return print_month_heat(df=b_data,val_bond=value)

@app.callback(
    Output(component_id='month_bar',component_property='figure'),
    Input(component_id='month_range',component_property='start_date'),
    Input(component_id='month_range',component_property='end_date'),
    Input(component_id='month_slider',component_property='value')
)
def month_bar_source(start_date,end_date,value):
    print(value)
    k_data = df.copy(deep=True)
    k_data = k_data[(k_data['datetime'] > start_date) & (k_data['datetime'] < end_date)]
    return print_month_bar(df=k_data, val_bond=value)
#App_start
if __name__ == '__main__':
    app.run_server(debug=True)