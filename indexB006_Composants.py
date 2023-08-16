"""
Dans ce script, on intervient sur différents composants

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)


# Configuration de la page @
app.layout = html.Div(children=[
    
    # Menu déroulant
    html.Label("Dropdown (menu déroulant)"),
    dcc.Dropdown(
        options=[ # Liste
            {'label':'New York City', 'value':'NYC'},
            {'label':'Montréal', 'value':'MTL'},
            {'label':'San Francisco', 'value':'SF'}],
        value='MTL' # Valeur par défaut
        ),
    
    # Menu déroulant avec une sélection multiple
    html.Label('Multi-select Dropdwon (menu déroulant sélection multiple)'),
    dcc.Dropdown(
        options=[ # Liste
            {'label':'New York City', 'value':'NYC'},
            {'label':'Montréal', 'value':'MTL'},
            {'label':'San Francisco', 'value':'SF'}],
        value='MTL', # Valeur par défaut
        multi=True
        ),
    
    # Boutons d'option
    html.Label("Radio Items (Boutons d'option)"),
    dcc.RadioItems(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label':'Montréal', 'value':'MTL'},
            {'label':'San Francisco', 'value':'SF'}],
        value='MTL' # Valeur par défaut
        ),
    
    # Cases à cocher
    html.Label("Checkboxes (cases à cocher)"),
    dcc.Checklist(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label':'Montréal', 'value':'MTL'},
            {'label':'San Francisco', 'value':'SF'}],
        value=['MTL', 'SF'] # Valeurs par défaut
        ),
    
    # Zone de saisie
    html.Label("Text Input (zone de saisie)"),
    dcc.Input(value='MTL', type='text'),
    
    # Curseur
    html.Label('Slider (curseur)'),
    dcc.Slider(
        min=0, max=9,
        marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
        value=5
    )
], style={'columnCount':2})

if __name__ == '__main__':
    app.run_server(debug=True)
    