# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


data = {"temperature": {"timestamp": [], "temp": []}, "voltage": {"timestamp": [], "volt": []},
        "current": {"timestamp": [], "curr": []}, "level": {"timestamp": [], "lvl": []}}


def parse_line(line, text):
    return line.split(text)[1].replace(" ", "").split(",")[0]


def open_file(filename):
    file = open(filename, "r")
    return file.readlines()


def parse_log(lines, field):
    for line in lines:
        if field is "temperature" and "temperature:" in line:
            temperature = parse_line(line, "temperature:")
            data["temperature"]["temp"].append(temperature[:2] + '.' + temperature[2:])
            data["temperature"]["timestamp"].append(line.split(" ")[1].split(".")[0])
        elif field is "current" and "current_now" in line:
            current = parse_line(line, "current_now:")
            data["current"]["curr"].append(current.replace("\n", ""))
            data["current"]["timestamp"].append(line.split(" ")[1].split(".")[0])
        elif field is "voltage" and "voltage" in line:
            voltage = parse_line(line, "voltage:")
            data["voltage"]["volt"].append(voltage[:1] + '.' + voltage[1:])
            data["voltage"]["timestamp"].append(line.split(" ")[1].split(".")[0])
        elif field is "level" and "level:" in line:
            level = parse_line(line, "level:")
            data["level"]["lvl"].append(level)
            data["level"]["timestamp"].append(line.split(" ")[1].split(".")[0])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='TEMS Sense DashMonitor'),

    html.Div(children='''
        Logs retrieved from IMX using remote ADB. Built using Dash.
    ''',),

    html.Div([
        dcc.Graph(id='batt-graph'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        dcc.Graph(id='volt-graph'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # in milliseconds
        n_intervals=0
    )

])


@app.callback(Output('batt-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_batt_graph(n):
    data["temperature"]["temp"] = []
    data["level"]["lvl"] = []
    data["temperature"]["timestamp"] = []
    lines = open_file("log.txt")
    parse_log(lines, "temperature")
    parse_log(lines, "level")
    return {
        'data': [
            {'x': data["temperature"]["timestamp"], 'y': data["temperature"]["temp"], 'type': 'line',
             'name': 'Temperature'},
            {'x': data["level"]["timestamp"], 'y': data["level"]["lvl"], 'type': 'line', 'name': 'Level', 'yaxis': 'y2'}
        ],
        'layout': {
            'title': 'Battery Temperature (ºC) / Battery Level (%)',
            'yaxis': {'type': 'linear'},
            'yaxis2': {'type': 'linear', 'side': 'right', 'overlaying': 'y'},
            'xaxis': {'showgrid': True}
        }
    }


@app.callback(Output('volt-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_volt_graph(n):
    data["voltage"]["volt"] = []
    data["current"]["curr"] = []
    data["voltage"]["timestamp"] = []
    lines = open_file("log.txt")
    parse_log(lines, "voltage")
    lines = open_file("logA.txt")
    parse_log(lines, "current")
    return {
        'data': [
            {'x': data["voltage"]["timestamp"], 'y': data["voltage"]["volt"], 'type': 'line', 'name': 'Voltage'},
            {'x': data["voltage"]["timestamp"], 'y': data["current"]["curr"], 'type': 'line', 'name': 'Current',
             'yaxis': 'y2'},
        ],
        'layout': {
            'title': 'Battery Voltage (V) / Current (mA)',
            'yaxis': {'type': 'linear'},
            'yaxis2': {'type': 'linear', 'side': 'right', 'overlaying': 'y'},
            'xaxis': {'showgrid': True}
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
