"""
Lien : https://www.youtube.com/watch?v=ExRFHt5n8SQ&list=PLh3I780jNsiRZX9Yciw-OupsNDeByUBhZ&index=4
Cours : Dash Ag Grid - Adding Custom Components

Documentation sur cell renderer components :
https://dash.plotly.com/dash-ag-grid/cell-renderer-components

Fichier complémentaire de même nom en javascript dans le répertoire 'assets'

Date : 22-11-2023
"""

import dash_ag_grid as dag
from dash import Dash, html, callback, Output, Input
import dash_bootstrap_components as dbc 
import pandas as pd   
import plotly.express as px
import json

# BACK END ------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/finance_survey.csv")

# TCD champ 'Objective' avec la moyenne des valeurs des champs 'Age' et 'Money'
subset = df.groupby("Objective")[["Age","Money"]].mean().reset_index()

# Arrondi des champs numériques
subset[["Age","Money"]] = subset[["Age","Money"]].round(0)

# Renommage des champs
subset.rename(columns={'Age': 'avg-Age', 'Money': 'avg-Money'}, inplace=True)

print(subset)

# Nouveau champ
subset['Graphing'] = ''

for i, r in subset.iterrows():
    
    filterDf = df[df["Objective"] == r["Objective"]]
    
    # fig = px.histogram(
    #     filterDf, # Données de la DF filtrée ci-avant
    #     x='Source', # Axe des x
    #     y='Money', # Axe des y
    #     )
    
    # Configuration du graphique : nuage de points
    fig = px.scatter(
        filterDf, # Données de la DF filtrée ci-avant
        x='Age', # Axe des x
        y='Money', # Axe des y
        color='Gender', # couleur selon le champ 'Gender'
        hover_data={'Money':True, # Données affichées lors du survol
                    'Age':True, 
                    'Gender':False,
                    })
    fig.update_layout(
        scattermode='group',
        scattergap=0.25,
        showlegend=False, # Afficher la légende
        yaxis_visible=False,
        yaxis_showticklabels=False,
        xaxis_visible=False,
        xaxis_showticklabels=False,
        margin=dict(l=0, r=0, t=0, b=0),
        template="plotly_dark",
    )
    
    subset.at[i, "Graphing"] = fig

# Configuration des colonnes de la table
columnDefs = [
    {
        "headerName": "avg-Age", # Nom de la colonne
        "field": "avg-Age", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
    },
    {
        "headerName": "avg-Money", # Nom de la colonne
        "field": "avg-Money", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
    },
    {
        "headerName": "Objective", # Nom de la colonne
        "field": "Objective", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Graphing", # Nom de la colonne
        "field": "Graphing", # ID de la colonne (même nom que l'en-tête)
        "cellRenderer": "DCC_GraphClickData", # Type d'icône
        "maxWidth": 900, # Taille max de l'icône
        "minWidth": 500, # Taille min de l'icône

    },
]

# Configuration de la table
table = dag.AgGrid(
    id="portfolio-table", # pour le callback
    className="ag-theme-alpine-dark", # thème
    columnDefs=columnDefs, # Configuration ci-avant
    rowData=subset.to_dict('records'), # données de la table
    columnSize="sizeToFit", # Colonnes ajustées à leurs largeurs
    dashGridOptions={"rowHeight": 120},
)

# FRONT END -----------------------------------------------------------

# Instanciation de la libraire et mise en page @
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Configuration de la page @
app.layout = dbc.Container(
    [   
        # Titre principal
        html.Div("Investments Survey", # Texte
                 className="h3 p-2 text-white bg-secondary", # Mise en forme
                 ),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [   
                                        # Table
                                        table, 
                                        
                                        # Zone vide
                                        html.Div(id='custom-component-graph-output')
                                    ]
                                ),
                            ],
                        )
                    ], width={"size": 10, "offset": 1},
                ),
            ],
            className="py-4",
        ),
    ],
)

# INTERACTION DES COMPOSANTS ---------------------------------------------

@callback(
    Output("custom-component-graph-output", "children"), # Sortie : zone vide
    Input("portfolio-table", # Entrée : table
          "cellRendererData", # Fonctionnalité : image insére
          )
)
def graphClickData(d):
    
    return json.dumps(d)


if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
