"""
Dans ce script, on intervient sur l'intéraction des widgets avec le callback

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Zone de saisie
    dcc.Input(
        id='my-id', 
        value='Initial value',
        type='text'),
    
    # Texte vide
    html.Div(
        id='my-div',
        children='')
])

@app.callback(
    Output( # Sortie : texte
        component_id='my-div', 
        component_property='children'),
    [Input( # Entrée : zone de saisie
        component_id='my-id',
        component_property='value')])
def update_output_div(input_value): # 1 argument = 1 entrée
    return f"Vous avez saisi {input_value}" # 1 variable en return = 1 sortie

if __name__ == '__main__':
    app.run_server(debug=True)
    