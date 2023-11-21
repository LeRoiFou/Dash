"""
Lien : https://www.youtube.com/watch?v=MzmefjD9Oow&list=PLh3I780jNsiRZX9Yciw-OupsNDeByUBhZ&index=3  
Cours : Dash Ag Grid - Icons, Dropdowns, and Links

Documentation sur le menu déroulant : 
https://dashaggrid.pythonanywhere.com/components/row-menu

Dans ce cours on apprend à insérer des menus déroulants, des icônes et des liens

Date : 21-11-2023
"""
import dash_ag_grid as dag             
from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd  

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Ag-Grid/row-deletion/finance_survey.csv")

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Ajout des images directement sur Dash sans passer par la DF chargée ci-avant
# (insertion des images sous le style markdown pour les liens)
danger = f"![dangerous market]({app.get_asset_url('prohibited.png')})"
safety =  f"![safe market]({app.get_asset_url('safe.png')})"

# Assignation d'une liste pour ajouter les icônes dans la DF
market_icons = []

# Pour chaque données du champ 'Stock_Market' de la DF...
for x in df.Stock_Market:
    
    # Si la valeur est 'No'...
    if x == 'No':
        # Ajout dans la liste de la donnée configurée ci-avant
        market_icons.append(f"{danger}")
    else:
        market_icons.append(f"{safety}")

# MAJ de la DF champ 'Stock_Market' selon la liste complétée ci-avant
df.Stock_Market = market_icons

# Ajout de liens : assignation d'une liste
linked_source = []

# Pour chaque données du champ 'Source' de la DF...
for x in df.Source:
    # Si la données est "Newspapers"...
    if x == 'Newspapers':
        # Ajout dans la liste du lien ci-après (style markdown pour le lien)
        linked_source.append(f'[{x}](https://www.lefigaro.fr/)')
    elif x == 'Television':
        linked_source.append(f'[{x}](https://www.nationalgeographic.com/tv/)')
    else:
        linked_source.append(f'[{x}](https://www.google.com/)')

# MAJ de la DF champ 'Source' selon la liste complétée ci-avant
df.Source = linked_source

# Configuration des colonnes de la table
columnDefs = [
    {
        "headerName": "Gender", # Nom de la colonne
        "field": "Gender", # ID de la colonne (même nom que l'en-tête)
        "checkboxSelection": True, # Case de sélection
        "cellEditor": "agSelectCellEditor", # menu déroulant
        "cellEditorParams": { # données du menu déroulant
            "values": ["Female", "Male"],
        },                                 
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
        "cellRenderer": "markdown"  # Icônes à insérer
    },
    {
        "headerName": "Objective", # Nom de la colonne
        "field": "Objective", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Source", # Nom de la colonne
        "field": "Source", # ID de la colonne (même nom que l'en-tête)
        "cellRenderer": "markdown"  # Liens à insérer
    },
]

# Configuration des attributs de la table
defaultColDef = {
    "filter": True, # Filtre
    "floatingFilter": True, # Zone de saisie pour filtre
    "resizable": True, # Taille ajustable
    "sortable": True, # Trie
    "editable": True, # Données modifiables
    "minWidth": 125, # Taille mini par colonne
}

# Configuration de la table
table = dag.AgGrid(
    id="portfolio-table", # pour le callback
    className="ag-theme-alpine-dark", # thème
    columnDefs=columnDefs, # configuration ci-avant
    rowData=df.to_dict('records'), # configuration ci-avant
    columnSize="sizeToFit", # Colonnes ajustées à leurs largeurs
    defaultColDef=defaultColDef, # configuration ci-vant
    dashGridOptions={"undoRedoCellEditing": True, 
                     "rowSelection":"multiple",
                     },
)

# Configuration de la page @
app.layout = dbc.Container(
    [   
        # Titre principal de la page @
        html.Div(
            "AG Grid: Icons, Dropdown, Link", # Texte
            className="h3 p-2 text-white bg-secondary", # mise en forme
            ),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Table configurée ci-avant
                        table
                    ], width={"size": 10, "offset": 1},
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
