"""
Lien : https://www.youtube.com/watch?v=FuJOsZgo4nU&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=4
Cours : Bar Graph (RadioItems) - Python Dash Plotly

Documentation plotly.express.bar : 
https://plotly.com/python-api-reference/generated/plotly.express.bar.html#plotly.express.bar

Documentation dcc.RadioItems :
https://dash.plotly.com/dash-core-components/radioitems

Documentation : 
https://plotly.com/python/reference/#layout-xaxis

Présentation d'un diagramme en barres : 
L'un des axes comporte généralement des valeurs numériques et l'autre décrit 
les types de catégories comparées

Date : 13-10-23
"""

import pandas as pd
import datetime as dt
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px

# DS -----------------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Urban_Park_Ranger_Animal_Condition_Response.csv")

# Filtres opérés sur la DF
df = df[(df['# of Animals'] > 0 ) 
        & (df['Age']!='Multiple')]

# Conversion du champ 'Date and Time of initial call' en type datetime
df['Month of Initial Call'] = pd.to_datetime(df['Date and Time of initial call'])

# Récupération uniquement du mois
df['Month of Initial Call'] = df['Month of Initial Call'].dt.strftime('%m')

# Copie du champ '# of Animals'
df['Amount of Animals'] = df['# of Animals']

# Copie du champ 'Duration of Response'
df['Time Spent on Site (hours)'] = df['Duration of Response']

# FRONT END --------------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([

        html.Div([
            
            # Titre principal de la page @
            html.Pre(
                children= "NYC Calls for Animal Rescue", # Texte
                style={"text-align": "center", # Alignement
                       "font-size":"100%", # Etirement
                       "color":"black",}, # Couleur du texte
                )
        ]),

        html.Div([
            
            # Titre rattaché au composant ci-après
            html.Label(
                ['X-axis categories to compare:'], # Texte
                style={'font-weight': 'bold'}, # Gras
                ),
            
            # Boutons d'option n° 1
            dcc.RadioItems(
                id='xaxis_raditem', # pour le callback
                options=[ # valeurs et données à afficher
                         {'label': 'Month Call Made', 
                          'value': 'Month of Initial Call'},
                         {'label': 'Animal Health', 
                          'value': 'Animal Condition'},
                ],
                value='Animal Condition', # Sélection par défaut
                style={"width": "50%"}, # Elargissement
            ),
        ]),

        html.Div([
            
            # Retour chariot
            html.Br(),
            
            # Titre rattaché au composant ci-après
            html.Label(
                ['Y-axis values to compare:'], # Texte
                style={'font-weight': 'bold'}, # Gras
                ),
            
            # Bouton d'option n° 2
            dcc.RadioItems(
                id='yaxis_raditem', # pour le callback
                options=[ # valeurs et données à afficher
                         {'label': 'Time Spent on Site (hours)', 
                          'value': 'Time Spent on Site (hours)'},
                         {'label': 'Amount of Animals', 
                          'value': 'Amount of Animals'},
                ],
                value='Time Spent on Site (hours)', # Sélection par défaut
                style={"width": "50%"}, # Elargissement
            ),
        ]),

    html.Div([
        
        # Graphique vide
        dcc.Graph(id='the_graph',),
    ]),

])

#INTERACTION ENTRE LES COMPOSANTS ----------------------------------------------

# MAJ du diagramme en barres selon les valeurs choisies dans les boutons d'option
@callback(
    Output( # Sortie : graphique
        component_id='the_graph', 
        component_property='figure'),
    [Input( # Entrée : Boutons d'option n° 1
        component_id='xaxis_raditem', 
        component_property='value'),
     Input( # Entrée : Boutons d'option n° 2
         component_id='yaxis_raditem', 
         component_property='value')]
)
def update_graph(x_axis, y_axis):

    # Copie de la DF
    dff = df
    # print(dff[[x_axis,y_axis]][:1])

    # MAJ du graphique (diagramme en barres)
    barchart=px.bar(
            data_frame=dff, # Récupération des données de la DF
            x=x_axis, # Axe x : récup valeur choisie boutons d'options n° 1
            y=y_axis, # Axe x : récup valeur choisie boutons d'options n° 2
            title=y_axis+': by '+x_axis, # Titre
            # facet_col='Borough', # Autant de graphique que de valeurs
            # color='Borough', # couleurs par rapport aux valeurs
            # barmode='group',
            )

    barchart.update_layout(
        xaxis={'categoryorder':'total ascending'}, # Trie croissant axe x
        title={'xanchor':'center', # Configuration du titre du graphique
               'yanchor': 'top', 
               'y':0.9,
               'x':0.5,
               })

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)
