"""
Lien : https://www.youtube.com/watch?v=ExRFHt5n8SQ&list=PLh3I780jNsiRZX9Yciw-OupsNDeByUBhZ&index=4
Cours : Dash Ag Grid - Adding Custom Components

Documentation sur cell renderer components :
https://dash.plotly.com/dash-ag-grid/cell-renderer-components

Fichier complémentaire de même nom en javascript dans le répertoire 'assets'
L'instruction cellrendere permet de mettre en forme un bouton en argumentant
les données à partir du fichier javascript situées dans le réppertoire 'assets'

Date : 22-11-2023
"""

import dash_ag_grid as dag    
from dash import Dash, html, callback, Input, Output, no_update, Patch
import dash_bootstrap_components as dbc
import pandas as pd      

# BACK END ------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/finance_survey.csv")

# Nouveau champ avec les mêmes données que le champ 'Invest'
df['Invest'] = 'sell'

# Configuration des colonnes de la table
columnDefs = [
    {
        "headerName": "Gender", # Nom de la colonne
        "field": "Gender", # ID de la colonne (même nom que l'en-tête)
        "checkboxSelection": True, # Case de sélection
    },
    {
        "headerName": "Age", # Nom de la colonne
        "field": "Age", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Filtre type numérique
    },
    {
        "headerName": "Money", # Nom de la colonne
        "field": "Money", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Filtre type numérique
    },
    {
        "headerName": "Stock_Market", # Nom de la colonne
        "field": "Stock_Market", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Objective", # Nom de la colonne
        "field": "Objective", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Source", # Nom de la colonne
        "field": "Source", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Invest", # Nom de la colonne
        "field": "Invest", # ID de la colonne (même nom que l'en-tête)
        "cellRenderer": "Button", # Icônes à insérer (voir fichier JS)
        "cellRendererParams": {"className": "btn btn-info"}, # Couleur icône
    },
]

# Configuration des attributs de la table
defaultColDef = {
    "filter": True, # Filtre
    "floatingFilter": True, # Zone de saisie pour le filtre
    "resizable": True, # Taille ajustable
    "sortable": True, # Trie
    "editable": True, # Données modifiables
    "minWidth": 125, # Taille mini par colonne
}


# Configuration de la table
table = dag.AgGrid(
    id="portfolio-table", # pour le callback
    className="ag-theme-alpine-dark", # thème
    columnDefs=columnDefs, # Configuration faite ci-avant
    rowData=df.to_dict('records'), # Alimentation des données de la DF
    columnSize="sizeToFit", # Colonnes ajustées à leurs largeurs
    defaultColDef=defaultColDef, # Configuration faite ci-avant
    dashGridOptions={"undoRedoCellEditing": True, 
                     "rowSelection":"multiple",
                     },
)

# FRONT END -------------------------------------------------------------

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
                                        # Table configurée ci-avant
                                        table,
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

# TODO
@callback(
    Output("portfolio-table", # Sortie : table
           "rowData" # Fonctionnalités : données de la table
           ), 
    Input("portfolio-table", # Entrée table : 
          "cellRendererData" # Fonctionnalités : icône inséré
          ), 
)
def showChange(n):
    
    # TODO
    if n:
        
        print(n)
        
        row_id_sold = int(n['rowId'])
        
        patched_table = Patch()
        
        patched_table[row_id_sold]['Money'] = 0
        
        return patched_table
    
    else:
        
        return no_update


if __name__ == "__main__":
    app.run_server(debug=True)
