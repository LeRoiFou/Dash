"""
Lien : https://community.plotly.com/t/dash-ag-grid-export-data-as-excel/77325/2

Recours au style configuré au niveau des en-têtes du fichier Excel

Date : 19-12-2023
"""

import dash_ag_grid as dag
from dash import Dash, html, Input, Output, clientside_callback
import pandas as pd

# BACK END ---------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

# Style attribué pour le fichier Excel an niveau des en-têtes UNIQUEMENT
excelStyles = [
    {
        "id": "header",
        "alignment": {
            "vertical": "Center", # alignement
        },
        "interior": {
            "color": "#f8f8f8", # couleur par défaut des cellules
             "patternColor": "undefined",
        },
        "borders": {
            "borderBottom": {
                "color": "#ffab00", # couleur de la bordure
                "lineStyle": "Continuous", # style de la bordure
                "weight": 1, # épaisseur de la bordure
            },
        },
    },
    {
        "id": "headerGroup",
        "font": {
            "bold": "true", # texte en gras
        },
    },
    {
        "id": "gold-header",
        "interior": {
            "color": "#E4AB11", # Couleur de la cellule
            "pattern": "Solid",
        },
    },
    {
        "id": "silver-header",
        "interior": {
            "color": "#bbb4bb", # Couleur de la cellule
            "pattern": "Solid",
        },
    },
    {
        "id": "bronze-header", 
        "interior": {
            "color": "#be9088", # Couleur de la cellule
            "pattern": "Solid",
        },
    },
]

# Configuration des en-têtes de la table
columnDefs = [
    {"field": "athlete"},
    {"field": "sport", "minWidth": 150},
    {
        "headerName": "Medals",
        "children": [
            {"field": "gold", "headerClass": "gold-header"},
            {"field": "silver", "headerClass": "silver-header"},
            {"field": "bronze", "headerClass": "bronze-header"},
        ],
    },
]

# Configuration de la table
defaultColDef = {
    "sortable": True, # Trie
    "filter": True, # Filtre
    "resizable": True, # Taille ajustable
    "minWidth": 100, # Taille mini
}

# FRONT END -------------------------------------------------------

# Instanciation de la librairie
app = Dash()


# Configuration de la page @
app.layout = html.Div(
    [   
        # Bouton d'export
        html.Button("Export to Excel", # Titre
                    id="btn-excel-header-style", # pour le callback
                    ),
        
        # Table
        dag.AgGrid(
            id="grid-excel-header-style", # pour le callback
            rowData=df.to_dict("records"), # données de la table
            columnDefs=columnDefs, # config des en-têtes effectuée ci-avant
            defaultColDef=defaultColDef, # configuration de la table ci-avant
            dashGridOptions={ # Configuration export Excel
                "excelStyles": excelStyles, # style pour l'export
                "defaultExcelExportParams": {"headerRowHeight": 30},
                # "headerRowHeight" : Défaut hauteur en-têtes 
            },
            enableEnterpriseModules=True, # indispensable pour l'export Excel
           
        ),
    ],
    className="excel-header-style",
)

# INTERACTION DES COMPOSANTS ------------------------------------------

# Configuration export Excel
clientside_callback(
    """function (n) {
        if (n) {
            dash_ag_grid.getApi("grid-excel-header-style").exportDataAsExcel();
        }
        return dash_clientside.no_update
    }""",
    Output("btn-excel-header-style", "n_clicks"),
    Input("btn-excel-header-style", "n_clicks"),
    prevent_initial_call=True, # évite MAJ des composants dès chargement page @
)


if __name__ == "__main__":
    app.run(debug=True)