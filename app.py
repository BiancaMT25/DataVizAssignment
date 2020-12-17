# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from my_graph_funcs import avg_lap_speed_ts, engine_barplot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_ts = pd.read_csv(r"graph_data\avg_lap_speed.csv")
min_speeds = pd.read_csv(r"graph_data\min_speeds.csv")
max_speeds = pd.read_csv(r"graph_data\max_speeds.csv")

df_engine = pd.read_csv(r"graph_data\top3.csv")
df_engine_exp = pd.read_csv(r"graph_data\top3_exp.csv")
df_engine_count = pd.read_csv(r"graph_data\engine_count_top3.csv")

unique_constructors = df_ts['constructorRef_mapped'].unique()
champions2020 = ['mercedes', 'red_bull', 'racing_point']

engine_fig = engine_barplot(df_engine, df_engine_exp, df_engine_count)

app.layout = html.Div(children=[
    html.H1(children='The Heart of a Car is its Engine'),
    html.H3(children='''
    Visualising Engine Effect on Formula 1 Race Cars
    '''),
    html.Div([

        html.Div([
            html.Label('Select Constructors'),
            dcc.Dropdown(
                id='avg-lap-speed-constructor',
                options=[{'label': i, 'value': i} for i in unique_constructors],
                value=champions2020,
                multi=True

            ),
        ], style={'width': '49%', 'display': 'inline-block'}),

    ], style={
        #'borderBottom': 'thin lightgrey solid',
        #'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(id='avg-lap-speed-ts'),
        dcc.Graph(id='engine-barplot', figure=engine_fig),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
])


@app.callback(
    dash.dependencies.Output('avg-lap-speed-ts', 'figure'),
    [dash.dependencies.Input('avg-lap-speed-constructor', 'value')])
def update_graph(constructors):
    dff = df_ts.loc[df_ts.constructorRef_mapped.isin(constructors)]
    fig = avg_lap_speed_ts(dff, max_speeds, min_speeds)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
