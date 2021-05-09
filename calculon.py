import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import calclib as cl

current_func = ''

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
    html.H2(children='F(x)',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            },
            id ='func_out'
            ),
    dcc.Graph(id='graph1'),
    html.Div('Please input a function of x', style={'color': '#ef3e18', 'margin':'10px'}),
    html.Div(children=[
        html.Label('Input Function:'),
        dcc.Input(id='input1', placeholder='Type a function of x here...',maxLength=50, value='x^2'),
        html.Label('Lower Bound:'),
        dcc.Input(id='input2', placeholder='Lower Bound', value= -100),
        html.Label('Upper Bound:'),
        dcc.Input(id='input3', placeholder='Upper Bound', value= 100),
        html.Label('Delta x:'),
        dcc.Input(id='input4', placeholder='Delta x', value= 1),
        dcc.Dropdown(
            id='dropdown1',
            options=[
                {'label': 'f(x)', 'value': 'op1'},
                {'label': 'f(x) and derivative', 'value': 'op2'},
                {'label': 'f(x) and two derivatives', 'value': 'op3'}
            ],
            value='op1'
        )
    ]),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H1(children='Limit Evaluator',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div(children=[
        dcc.Input(id='input5', placeholder='Enter an x value',maxLength=50),
    ]),
    html.Div(children=[
        html.Label('Positive Limit: ', id='output1'),
        html.Label('Negative Limit: ', id='output2')
    ])
])

@app.callback(
        Output('func_out', 'children'),
        Input('input1', 'value'))
def update_function(input):
    return input

@app.callback(Output('graph1', 'figure'),
              Input('func_out', 'children'))
def update_graph(input):
    try:
        temp = cl.decompose(input)
        print(temp)
        func = cl.format(temp)
        print(func)
        data = cl.evalRange(func, -10, 10, 1)
        print(data)
        df = pd.DataFrame(np.array(data), columns=['x', 'y'])
        output = [go.Scatter(x=df['x'], y=df['y'], mode='lines', name=input, showlegend=False)]
        return {'data': output, 'layout': go.Layout(title='F(x)= ' + str(input),
                                                      xaxis={'title': 'x'},
                                                      yaxis={'title': 'F(x)'})}
    except:
        return {'data': [], 'layout': go.Layout(title='Invalid Expression',
                                                    xaxis={'title': 'x'},
                                                    yaxis={'title': 'F(x)'})}


if __name__ == '__main__':
    app.run_server()