"""
Lien : https://www.youtube.com/watch?v=iV51JqP6y_Q&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R
Cours : Pie Chart (Dropdowns) - Python Dash Plotly

Documentation sur dcc.Dropdown :
https://dash.plotly.com/dash-core-components/dropdown

Liste des différents graphiques :
https://plotly.com/python-api-reference/plotly.express.html

MAJ du graphique (camembert) à partir d'un menu déroulant

Date : 11-10-23
"""
from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Urban_Park_Ranger_Animal_Condition_Response.csv")

# FRONT END -----------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
    html.Div([
        
        # Titre rattaché au menu déroulant
        html.Label(['NYC Calls for Animal Rescue']),
        
        # Menu déroulant
        dcc.Dropdown(
            id='my_dropdown', # pour le callback
            options=[ # valeurs pour le menu déroulant
                     {'label': 'Action Taken by Ranger', 
                      'value': 'Final Ranger Action'},
                     {'label': 'Age', 'value': 'Age'},
                     {'label': 'Animal Health', 'value': 'Animal Condition'},
                     {'label': 'Borough', 'value': 'Borough'},
                     {'label': 'Species', 'value': 'Animal Class'},
                     {'label': 'Species Status', 'value': 'Species Status'}
            ],
            value='Animal Class', # valeur affichée par défaut -> label : 'Species'
            multi=False, # pas de possibilité d'afficher plusieurs valeurs
            clearable=False, # pas de possib de supprimer les valeurs affichées
            style={"width": "50%"} # largeur du menu déroulant
        ),
    ]),

    html.Div([
        
        # Graphique vide
        dcc.Graph(id='the_graph')
    ]),

])

# INTERACTION DES COMPOSANTS -----------------------------------------------

# Selon la valeur sélectionnée dans le menu déroulant, MAJ du camembert
@callback(
    Output( # Sortie : graphique
        component_id='the_graph', component_property='figure'
        ),
    [Input( # Entrée menu déroulant
        component_id='my_dropdown', component_property='value'
        )]
)
def update_graph(my_dropdown):
    
    # Copie de la DF
    dff = df

    # MAJ du camembert
    piechart=px.pie(
            data_frame=dff, # Données de la DF
            names=my_dropdown, # filtre sur le champ de la DF
            hole=.3, # Largeur du trou central du camembert
            )

    return (piechart)


if __name__ == '__main__':
    app.run_server(debug=True)

