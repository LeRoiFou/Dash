"""
Dans ce script, on intervient sur les tables de DF

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
import pandas as pd

# Récupération du fichier CSV converti en DF pandas
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

def generate_table(dataframe, max_row=10):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_row))]
    )

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Sous-titre
    html.H4(children='US Agriculture Exports (2011)'),
    
    # Récupération de la DF
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
    