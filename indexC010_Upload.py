"""
Lien : https://www.youtube.com/watch?v=6W4HpSI20NM&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=12
Cours : The Upload Component - Plotly Dash

Documentation sur le composant Upload :
https://dash.plotly.com/dash-core-components/upload

Fichier utilisé pour ce tuto : Caste.csv

Date : 10-09-2023
"""

import base64
import datetime
import io
from dash import (Dash, Input, Output, State, html, dash_table, dcc, callback, 
                  no_update) # no_update : composant à ne pas afficher
import plotly.express as px
import pandas as pd

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie
app = Dash(__name__, 
           external_stylesheets=external_stylesheets, # Mise en forme
           # L'instruction ci-après est à insérer lorsque les composants
           # s'affichent dynamiquement après intervention sur un composant
           # https://stackoverflow.com/questions/67546867/whats-the-role-of-suppress-callback-exceptions-in-dash-python
           suppress_callback_exceptions=True,
           )

# Configuration de la page @
app.layout = html.Div([
    
    # Composants pour charger les fichiers
    dcc.Upload(
        id='upload-data', # Pour le callback
        children=html.Div([
            'Drag and Drop or ', # Déplacer le fichier à charger dans ce composant
            html.A('Select Files') # ou ouverture d'une boîte de dialogue
        ]),
        style={ # Style du composant
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True # Autorisation de charger plusieurs fichiers
    ),
    
    # Zone vide pour le graphique (voir 2ème callback)
    html.Div(id='output-div'),
    
    # Zone vide pour la datatable (voir 1er callback)
    html.Div(id='output-datatable'),
])

def parse_contents(contents, filename, date):
    
    # Chargement du fichier : script type du site @ Dash
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Si le fichier à charger est de type .csv
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        # Si le fichier à charger est de type .xls   
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    # Si le fichier n'est ni de type .csv ou de type .xls
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # Incidences sur la page @
    return html.Div([
        
        # Titre : nom du fichier
        html.H5(filename),
        
        # Date et heure du fichier
        html.H6(datetime.datetime.fromtimestamp(date)),
        
        # Libellé
        html.P("Inset X axis data"),
        
        # Menu déroulant récupérant les en-têtes de la dataframe
        dcc.Dropdown(id='xaxis-data', # pour le callback
                     options=[{'label':x, 'value':x} for x in df.columns]),
        
        # Libellé
        html.P("Inset Y axis data"),
        
        # Menu déroulant récupérant les en-têtes de la dataframe
        dcc.Dropdown(id='yaxis-data', # pour le callback
                     options=[{'label':x, 'value':x} for x in df.columns]),
        
        # Bouton
        html.Button(id="submit-button", # pour le callback
                    children="Create Graph"), # titre du bouton
        
        # Saut de ligne
        html.Hr(),

        # Data table
        dash_table.DataTable(
            data=df.to_dict('records'), # alimentation des données de la DF
            columns=[{'name': i, 'id': i} for i in df.columns], # Entêtes + callback
            page_size=15 # nombre de lignes
        ),
        
        # Au choix du graphique à afficher, mais attention ce composant est
        # limité à une certaine taille des données à traiter, donc composant
        # à déconseiller à utiliser
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        # Saut de ligne
        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# Affichage dans une datatable du contenu des fichiers chargés avec le composant
# upload
@callback(Output('output-datatable', 'children'), # Sortie : datatable
              Input('upload-data', 'contents'), # Entrée : upload - contenu
              State('upload-data', 'filename'), # Upload - nom du fichier
              State('upload-data', 'last_modified')) # Upload - dernière modif
def update_output(list_of_contents, list_of_names, list_of_dates): # 3 entrées
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# Affichage d'un graphique (diagramme en bar) généré à partir du bouton et des
# menu déroulants
@callback(Output('output-div', 'children'), # Sortie : zone vide pour graphique
              Input('submit-button','n_clicks'), # Entrée : bouton
              State('stored-data','data'), 
              State('xaxis-data','value'), # menu déroulant axe des x
              State('yaxis-data', 'value')) # menu déroulant axe des y
def make_graphs(n, data, x_data, y_data): # 4 entrées
    if n is None: # Si l'utilisateur n'appuie pas sur le bouton
        return no_update # pas de graphique à afficher
    else: # Sinon affichage du diagramme en barres
        bar_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return dcc.Graph(figure=bar_fig)

if __name__ == '__main__':
    app.run_server(debug=True)
