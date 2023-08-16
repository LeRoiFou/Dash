"""
Dans ce script, on intervient sur les rappels enchaînés :
la sortie d'une fonction de rappel peut-être l'entrée d'une autre fonction de rappel.

On a cette fois-ci recours à plusieurs callback

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

# Assignation d'un dictionnaire : capitales désignées dans des États différents
all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': ['Montréal', 'Toronto', 'Ottawa']
}

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Boutons d'option n° 1 (États)
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'),
    
    # Ligne séparatrice
    html.Hr(),
    
    # Boutons d'option n° 2 vide (capitales)
    dcc.RadioItems(id='cities-dropdown'),
    
    # Ligne séparatrice
    html.Hr(),
    
    # Texte vide
    html.Div(id='display-selected-values')
])

# Selon l'État sélectionné dans le widget Boutons d'option n° 1, les capitales
# rattachées à cette État, s'afficheront dans le widget Boutons d'option n° 2
@app.callback(
    Output('cities-dropdown', 'options'), # Sortie : Boutons d'option n° 2
    [Input('countries-dropdown', 'value')]) # Entrée : Boutons d'option n° 1
def set_cities_options(selected_country): # un argument = une entrée
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

# Selon la capitale sélectionnée, par défaut c'est toujours le 1er composant
# qui sera sélectionné
@app.callback(
    Output('cities-dropdown', 'value'), # Entrée : Boutons d'option n° 2
    [Input('cities-dropdown', 'options')]) # Sortie : Boutons d'option n° 2
def set_cities_value(available_options): # un argument = une entrée
    return available_options[0]['value']

# MAJ du texte : mention de l'État et de la capitale sélectionnée
@app.callback(
    Output('display-selected-values', 'children'), # Sortie : texte vide
    [Input('countries-dropdown', 'value'), # Entrée n° 1 : Boutons d'option n° 1
     Input('cities-dropdown', 'value')]) # Entrée n° 2 : Boutons d'option n° 2
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


if __name__ == '__main__':
    app.run_server(debug=True)
    