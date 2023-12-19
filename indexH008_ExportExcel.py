"""
Export d'un tableau Ag Grid sous Excel :
https://community.plotly.com/t/dash-ag-grid-export-data-as-excel/77325/2

Exportation d'un tableau Ag Grid sous Excel

Date : 19-12-23
"""

import dash_ag_grid as dag
from dash import Dash, html, Input, Output, clientside_callback # export Excel
import pandas as pd

# BACK END -------------------------------------------------------------

# Récupération du fichier .csv converti en df pandas
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

# Configuration des entêtes du tableau
columnDefs = [
    {
        "headerName": "Athlete Details",
        "children": [
            {"field": "athlete", "width": 180},
            {"field": "age", "width": 90},
            {"field": "country", "width": 140},
        ],
    },
    {
        "headerName": "Sports Results",
        "children": [
            {"field": "sport", # nom du champ
             "width": 140, # Taille du champ
             },
            {"field": "total", # nom du champ
             "width": 100, # Taille du champ
             "filter": "agNumberColumnFilter", # Filtre numérique
             "columnGroupShow": "closed", # colonne affichée
             },
            {"field": "gold", # nom du champ
             "width": 100, # Taille du champ
             "filter": "agNumberColumnFilter", # Filtre numérique
             "columnGroupShow": "open", # colonne masquée
             },
            {"field": "silver", # nom du champ
             "width": 100, # Taille du champ
             "filter": "agNumberColumnFilter", # Filtre numérique
             "columnGroupShow": "open", # colonne masquée
             },
            {"field": "bronze", # nom du champ
             "width": 100, # Taille du champ
             "filter": "agNumberColumnFilter", # Filtre numérique
             "columnGroupShow": "open", # colonne masquée
             },
        ],
    },
]

# FRONT END -------------------------------------------------------

# Instanciation de la librairie
app = Dash()

# Configuration de la page @
app.layout = html.Div(
    [   
        # Bouton d'exécution
        html.Button("Export to Excel", # Titre du bouton
                    id="btn-excel-export", # pour le callback
                    ),
        
        # Tableau
        dag.AgGrid(
            id="grid-excel-export", # pour le callback
            rowData=df.to_dict("records"), # données du tableau
            columnDefs=columnDefs, # en-têtes des champs configurés ci-avant
            defaultColDef={"resizable": True, # Taille ajustable
                           "filter": True, # Filtre
                           },
            enableEnterpriseModules=True, # Indispensable pour l'export Excel
        ),
    ]
)

# INTERACTION DES COMPOSANTS ---------------------------------------------

# Export sous Excel (callback sans fonction !)
clientside_callback(
    """function (n) {
        if (n) {
            dash_ag_grid.getApi("grid-excel-export").exportDataAsExcel();
        }
        return dash_clientside.no_update
    }""",
    Output("btn-excel-export", "n_clicks"),
    Input("btn-excel-export", "n_clicks"),
    prevent_initial_call=True
    # pas de MAJ des composants attendus en sortie dès chargement de la page @
)


if __name__ == "__main__":
    app.run(debug=True)
