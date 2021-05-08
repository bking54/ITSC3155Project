import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import calclib as cl

df = pd.DataFrame(np.array([[1,1], [4,4], [9,9]]), columns=['x','y'])
data = [go.Scatter(x=df['x'], y=df['y'], mode='lines', name='main_function', showlegend=False)]

app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.H1(children='Calculon Graphing Calculator',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for graphing functions using Python', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    dcc.Graph(id='graph1'),
    html.Div('Please input a function of x', style={'color': '#ef3e18', 'margin':'10px'}),
    html.Div(children=[
        dcc.Input(id='input1', placeholder='Type a function of x here...',maxLength=50),
        dcc.Dropdown(
            id='select-graph',
            options=[
                {'label': 'f(x)', 'value': 'op1'},
                {'label': 'f(x) and derivative', 'value': 'op2'},
                {'label': 'f(x) and all derivatives', 'value': 'op3'}
            ],
            value='op1'
        )
    ])
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-graph', 'value')])
def update_figure(selected_graph):
    print('update figure attempt')
    return {'data': data, 'layout': go.Layout(title='Graph of f(x)',
                                                          xaxis={'title': 'x'},
                                                          yaxis={'title': 'f(x)'})}


if __name__ == '__main__':
    app.run_server()