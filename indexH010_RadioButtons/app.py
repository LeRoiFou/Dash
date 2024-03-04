"""
Lien : https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Ag-Grid/filters/radio-button-filter.py
Cours : Filter Dash AG Grid with Radio Buttons

Dans ce cours, on filtre la table AgGrid selon l'option choisie dans le composant
des boutons d'options.
Le script du filtre est asses spécifique (ce n'est pas dy python)...

Date : 04-03-2024
"""

import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd

# BACK END -------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

# CONFIGURATION DES COMPOSANTS --------------------------------------

# Configuration des colonnes de la table AgGrid
columnDefs = [
    {"field": 'athlete',  # nom du champ
     "minWidth": 180, # largeur max
     },
    {"field": 'age',  # nom du champ
     "filter": 'agNumberColumnFilter', 
     "maxWidth": 80, # largeur max
     },
    {"field": 'country', # nom du champ
     },
    {"field": 'year',  # nom du champ
     "maxWidth": 90, # largeur max
     },
    {"field": 'date', # nom du champ
     "filter": 'agDateColumnFilter', # filtre sur ce champ
     "filterParams": { # paramétrage du filtre
            "comparator": {"function": "dateFilterComparator"},
        },
    },
]

# Filtre appliqué sur la table AgGrid
filter_function = {
    'below25': "params.data.age < 25",
    'between25and50': "params.data.age >= 25 && params.data.age <= 50",
    'above50': "params.data.age > 50",
    'everyone': "true"
}

# FRONT END -----------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash()

# Configuration de la page @
app.layout = html.Div(
    [
        # Boutons d'option
        dcc.RadioItems(
            id='external-filter-radio', # pour le callback
            options={ # Valeurs affichées
                'everyone': 'Everyone',
                'below25': 'Below 25',
                'between25and50': 'Between 25 and 50',
                'above50': 'Above 50',
            },
            value='everyone', # valeur par défaut sélectionnée
            inline=False,
            style={'margin': '10px'} # style attribué
        ),
        
        # Table AgGrid
        dag.AgGrid(
            id="external-filter-example", # pour le callback
            rowData=df.to_dict("records"), # données de la DF converties en dict
            columnDefs=columnDefs, # configuration des colonnes ci-vant
            defaultColDef={"flex": 1},
            # dashGridOptions={"isExternalFilterPresent":{"function":"true"},
            #                  "doesExternalFilterPass": {"function": filter_function['below25']}}
        ),
    ]
)

# INTERACTION DES COMPOSANTS ---------------------------------------------

# Filtre sur la table AgGrid selon la valeur sélectionnée dans les boutons d'option
@callback(
    Output( # Sortie : table AgGrid
        "external-filter-example", # id
        "dashGridOptions" # fonctionnalités : filtre
        ), 
    Input( # Entrée : boutons d'option
        "external-filter-radio", # id
        "value" # fonctionnalités : valeur sélectionnée des boutons d'option
        ),
    prevent_initial_call=True, # évite une erreur lors de la MAJ de la page @
)
def update_external_filter(filter_value):
    return {
        # if filter_value is not 'everyone', then we will start filtering
        # MAJ de la table AgGrid selon la valeur sélectionnée aux boutons d'option
        "isExternalFilterPresent": {
            "function": "true" if filter_value != 'everyone' else "false"},
        "doesExternalFilterPass": {
            "function": filter_function[filter_value]}
    }


if __name__ == "__main__":
    app.run(debug=True)
