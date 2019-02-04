# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

data = {"x": [], "y": []}
filename = "log4.txt"
file = open(filename, "r")
lines = file.readlines()

for line in lines:
    data["x"].append(line.split(" ")[1].split(".")[0])
    y = line.split("temperature: ")[1].split(",")[0]
    data["y"].append(y[:2] + '.' + y[2:])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Battery Temperature'),

    html.Div(children='''
        Logs retrieved from IMX using remote ADB. Built using Dash.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': data["x"],
                 'y': data["y"],
                 'type': 'line', 'name': 'Temp'},
            ],
            'layout': {
                'title': 'Battery Temperature',
                'yaxis': {'type': 'linear'},
                'xaxis': {'showgrid': False}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
