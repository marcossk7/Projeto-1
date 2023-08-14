import re
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import calculate_string_expression as cse

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

classname = 'border 2-p d-flex align-items-center justify-content-center'
stl = {'margin-top' : '10px', 'height': '10vh', 'width':'100%'}

lista_caracteres = [*[str(i) for i in range(0,10)], *['+', '-', '*', '/', '^', '(', ')']]
lista_botoes = [*[f'b-{str(i)}' for i in range(0,10)], *['b-soma', 'b-sub', 'b-mult', 'b-div', 'b-exp', 'b-paa', 'b-paf']]
dic_botoes = dict(zip(lista_caracteres, lista_botoes))


col1 = {
    'b-clearhist': '\U0001F5D1',
    'b-paa' :'(',
    'b-7' :'7',
    'b-4' :'4',
    'b-1' :'1',
    'b-dec' : html.Div(id="output-2", title='O último valor que digitar é o número de casas decimais.',children='')
}

col2 = {
    'b-cls' : 'C',
    'b-paf' :')',
    'b-8' :'8',
    'b-5' :'5',
    'b-2' :'2',
    'b-0' :'0'

}
col3 = {
    'b-porc' : '%',
    'b-exp' :'^',
    'b-9' :'9',
    'b-6' :'6',
    'b-3' :'3',
    'b-ponto' :'.'
}

col4 = {
    'b-eraser' : '\u232B',
    'b-soma' :'+',
    'b-sub' :'-',
    'b-mult' :'*',
    'b-div' :'/',
    'b-igual' : '='
}

no_buttons_return = {'b-clearhist', 'b-dec', 'b-porc', 'b-cls', 'b-eraser', 'b-igual'}
buttons = {**col1, **col2, **col3, **col4}

layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.B(children=['Calculadora 1.0'], className=classname, style={'margin-top' : '10px', 'height': '5vh', 'padding-right': '4px', 'font-size': '20px'}),
                html.Div(id="output", children='', className='border 2-p d-flex align-items-center justify-content-right', style={'margin-top' : '10px', 'height': '10vh', 'padding-left': '4px', 'border':'1px solid gray'}),
                dbc.Row([
                    dbc.Col([html.Button(v, id=f'{k}',  n_clicks=0, className=classname, style=stl) for k,v in col1.items()], width=3),
                    dbc.Col([html.Button(v, id=f'{k}',  n_clicks=0, className=classname, style=stl) for k,v in col2.items()], width=3),
                    dbc.Col([html.Button(v, id=f'{k}',  n_clicks=0, className=classname, style=stl) for k,v in col3.items()], width=3),
                    dbc.Col([html.Button(v, id=f'{k}',  n_clicks=0, className=classname, style=stl) for k,v in col4.items()], width=3),
                ])
            ], width=4, style={'display': 'flex', 'flexDirection': 'column'}),  
            
            dbc.Col([
                 html.B(children=['Histórico'], className=classname, style={'margin-top' : '10px', 'height': '5vh', 'padding-right': '4px', 'font-size': '20px'}),
                html.Div([ 
                    html.Ul(id='calculations-list', children=[], style={
                        'border': '2px solid gray',
                        'flex': 1,  
                        'overflowY': 'auto'
                    }),
                ], style={'margin-top' : '10px','flex': 1, 'display': 'flex', 'flexDirection': 'column'}),  
                dcc.Store(id='store-calculations', data=[])
            ], width=4, style={'display': 'flex', 'flexDirection': 'column'}),  
        ], style={'margin-top' : '4px','display': 'flex', 'flexDirection': 'row'}),  
    ], fluid=True)

@app.callback(
    [Output("output", "children"),
     Output('store-calculations', 'data'),
     Output('output-2', 'children')],
    [Input(k, "n_clicks") for k in buttons],
    [State("output", "children"),
     State('store-calculations', 'data'),
     State('output-2', 'children')]
)

# Funções dos callbacks
def update_output(*args):
    decimal_number = args[-1] 
    stored_calculations = args[-2]
    current_value = args[len(buttons)]
    button_action_dict = buttons
    ctx = callback_context
    
    if not ctx.triggered:
        button_id = "No clicks yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id in button_action_dict.keys() and button_id not in no_buttons_return:
        value_to_add = str(button_action_dict[button_id])
        current_value += value_to_add
    
    elif button_id == "b-cls":
        current_value = current_value[:-len(current_value)]

    elif button_id == "b-eraser":
        current_value = current_value[:-1]

    elif button_id == "b-clearhist":
        stored_calculations = []
    
    elif button_id == "b-porc":
        # find a mach
        match = re.search(r'^-?\d+(\.\d+)?$', current_value)

        # if have a mach
        if match:
            result = float(match.group().replace('%', '')) / 100
            if decimal_number == '':
                current_value = str(result)
            else:
                current_value = str(round(result, int(decimal_number)))
        else:
            current_value = 'error'

    elif button_id == "b-igual":
        result = cse.executor_operation_strings(current_value) # type = float
        expression = current_value
        if decimal_number == '':
            current_value = str(result)
        else:
            current_value = str(round(result, int(decimal_number)))
        stored_calculations.append(f'{expression} = {current_value}')


    if button_id == "b-dec":
        if current_value[-1].isnumeric():
            decimal_number = current_value[-1]
            current_value = current_value[:-1]

          
    
    return current_value, stored_calculations, decimal_number

@app.callback(
    Output('calculations-list', 'children'),
    [Input('store-calculations', 'data')]
)
def update_calculation_list(stored_calculations):
    return [html.Li(calculation) for calculation in stored_calculations]

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)