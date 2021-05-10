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
                'color': '#478DC2'
            }
            ),
    html.Div('Web dashboard for graphing functions using Python', style={'textAlign': 'center'}),
    html.Br(),
    html.Hr(style={'color': '#8BC2EC'}),
    html.H2(children='F(x)',
            style={
                'textAlign': 'center',
                'color': '#478DC2'
            },
            id ='func_out'
            ),
    dcc.Graph(id='graph1'),
    html.Div('Please input a function of x', style={'color': '#ef3e18', 'margin':'10px'}),
    html.Div(children=[
        html.Label('Input Function:'),
        dcc.Input(id='input1', placeholder='Type a function of x here...',maxLength=50, value='x^2'),
        html.Label('Lower Bound:'),
        dcc.Input(id='lbound', placeholder='Lower Bound', value= -100),
        html.Label('Upper Bound:'),
        dcc.Input(id='ubound', placeholder='Upper Bound', value= 100),
        html.Label('Delta x:'),
        dcc.Input(id='deltax', placeholder='Delta x', value= 1),
        dcc.Dropdown(
            id='dropdown1',
            options=[
                {'label': 'f(x) without derivative', 'value': 'op1'},
                {'label': 'f(x) and derivative', 'value': 'op2'}
            ],
            value='op1'
        )
    ]),
    html.Hr(style={'color': '#8BC2EC'}),
    html.H1(children='Limit Evaluator',
            style={
                'textAlign': 'center',
                'color': '#478DC2'
            }
            ),
    html.Div(children=[
        html.Label('Enter a value:'),
        dcc.Input(id='lim', placeholder='Enter an x value',maxLength=50, value=0),
    ]),
    html.Div(children=[
        html.Label('Positive Limit:'),
        dcc.Input(id = 'poslim', readOnly=True),
        html.Label('Negative Limit:'),
        dcc.Input(id= 'neglim', readOnly=True)
    ])
])

@app.callback(
        Output('func_out', 'children'),
        Input('input1', 'value'))
def update_function(input):
    return input

@app.callback(Output('graph1', 'figure'),
              Input('func_out', 'children'),
              Input('lbound', 'value'),
              Input('ubound', 'value'),
              Input('deltax', 'value'),
              Input('dropdown1', 'value'))
def update_graph(input, start, end, delta, option):
    try:
        start = int(start)
        end = int(end)
        delta = float(delta)
        temp = cl.decompose(input)
        func = cl.format(temp)
        data = cl.evalRange(func, start, end + 1, delta)
        df = pd.DataFrame(np.array(data), columns=['x', 'y'])
        output = [go.Scatter(x=df['x'], y=df['y'], mode='lines', name=input)]
        if (option == 'op2'):
            deriv = cl.getDerivative(data, input)
            df2 = pd.DataFrame(np.array(deriv), columns=['x', 'y'])
            deriv_out= go.Scatter(x=df2['x'], y=df2['y'], mode='lines', name='derivative')
            output.append(deriv_out)
        return {'data': output, 'layout': go.Layout(title='F(x)= ' + str(input),
                                                      xaxis={'title': 'x'},
                                                      yaxis={'title': 'F(x)'})}
    except:
        return {'data': [], 'layout': go.Layout(title='Invalid Expression',
                                                    xaxis={'title': 'x'},
                                                    yaxis={'title': 'F(x)'})}

@app.callback(Output('poslim', 'value'),
              Output('neglim', 'value'),
              Input('func_out', 'children'),
              Input('lim', 'value'))
def update_limit(func, xval):
    try:
        xval = float(xval)
        temp = cl.decompose(func)
        func = cl.format(temp)
        list = cl.limit(func, xval, 10)
        return list[0], list[1]
    except:
        return 'N/A', 'N/A'

if __name__ == '__main__':
    app.run_server()