"""
Dans ce script, on intervient sur l'intéraction des widgets avec le callback
-> L'entrée : le curseur
-> La sortie : le graphique
Selon l'année sélectionnée au curseur, le graphique se met à jour

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Récupération du fichier csv converti en DF pandas
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Graphique
    dcc.Graph(id='graph-with-slider'),
    
    # Curseur
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None)
])

# MAJ du graphique selon l'année sélectionnée au curseur
@app.callback(
    Output( # Sortie : graphique
        'graph-with-slider', 
        'figure'),
    [Input( # Entrée : curseur
        'year-slider', 
        'value')])
def update_figure(selected_year): # un argument = une entrée (le curseur)
    
    # Filtre sur la DF selon l'année sélectionnée au curseur
    filtered_df = df[df.year == selected_year]
    
    # Assignation d'une liste vide
    traces = []
    
    # MAJ du graphique selon l'année filtrée dans la DF
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i))
        
    # Retour d'une seule variable = une sortie (le graphique)
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest')}


if __name__ == '__main__':
    app.run_server(debug=True)
    