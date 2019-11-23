#!/usr/bin/python3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objects as go

from enviroplus import gas

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

nh3 = [1,2,3]
oxidising = [1,2,3]
reducing = [1,2,3]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Home monitor'),

    dcc.Graph(
        id='home-monitor',
    ),
    dcc.Interval(
        id='interval-component',
        interval=(1*1000)*60, # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('home-monitor', 'figure'),
                      [Input('interval-component', 'n_intervals')])
def update_graph(n):
    nh3.append(gas.read_nh3())
    oxidising.append(gas.read_oxidising())
    reducing.append(gas.read_reducing())

    traces = list()
    traces.append(plotly.graph_objs.Scatter(y=nh3,name='NH3',mode= 'lines+markers'))
    traces.append(plotly.graph_objs.Scatter(y=oxidising,name='Oxidising',mode= 'lines+markers'))
    traces.append(plotly.graph_objs.Scatter(y=reducing,name='Reducing',mode= 'lines+markers'))
    return {'data': traces}

if __name__ == '__main__':
    app.run_server(debug=True,  host='0.0.0.0')
