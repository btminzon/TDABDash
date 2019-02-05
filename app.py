# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def open_file(filename = "log.txt"):
    file = open(filename, "r")
    return file.readlines()


def parse_log(lines):
    data = {"timestamp": [], "temperature": []}
    for line in lines:
        if len(line.replace("  ", " ").split(" ")) > 15:
            data["timestamp"].append(line.split(" ")[1].split(".")[0])
            y = line.replace("  ", " ").split(" ")[14].replace(",", "")
            data["temperature"].append(y[:2] + '.' + y[2:])
    return data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Battery Temperature'),

    html.Div(children='''
        Logs retrieved from IMX using remote ADB. Built using Dash.
    '''),

    dcc.Graph(
        id='batt-graph'
    ),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # in milliseconds
        n_intervals=0
    )

])

@app.callback(Output('batt-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_batt_graph(n):
    lines = open_file()
    data = parse_log(lines)
    return {
        'data': [
            {'x': data["timestamp"],
             'y': data["temperature"],
             'type': 'line', 'name': 'Temp'},
        ],
        'layout': {
            'title': 'Battery Temperature',
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
