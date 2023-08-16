"""
Dans ce script, on intervient sur l'intéraction des widgets avec le callback,
en recourant cette fois-ci à des sorties multiples

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
        id='num',
        type='number',
        value=5),
    
    # Table
    html.Table([
        html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
        html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
        html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
        html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
        html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),]),
])

# Résultat au carré, à la puissance 3... selon la valeur dans la zone de saisie
@app.callback(
    [Output('square', 'children'), # Sortie 1 : x puissance 2 (table)
     Output('cube', 'children'), # Sortie 2 : x puissance 3 (table)
     Output('twos', 'children'), # sortie 3 : 2 puissance x (table)
     Output('threes', 'children'), # sortie 4 : 3 puissance x (table)
     Output('x^x', 'children')], # sortie 5 : x puissannce x (table)
    [Input('num', 'value')]) # Entrée : Zone de saisie
def callback_a(x): # un argument en paramètre = une entrée (zone de saisie)
    return x**2, x**3, 2**x, 3**x, x**x # 5 variables en retour = 5 sorties (table)


if __name__ == '__main__':
    app.run_server(debug=True)
    