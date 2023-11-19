"""
Lien : https://www.youtube.com/watch?v=T8t5DfXtXI0&list=PLh3I780jNsiRZX9Yciw-OupsNDeByUBhZ
Cours : Dash Ag Grid - Save Table Button

# Sauvegarde des données d'une table

Date : 19-11-2023
"""

import dash_ag_grid as dag          
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc 
import pandas as pd         
import os

# BACK END --------------------------------------------------------------------

# Assignation en liste des fichiers se trouvant dans le répertoire ci-après
# pour alimenter ces fichiers dans le menu déroulant
datasets = [files for path, subdirectory, files in os.walk(
    "\\Users\\LRCOM\\pythonProjects\\dash\\data")]

# Liste des fichiers dans le répertoire désigné ci-avant
print(datasets[0])

# Configuration des colonnes de la table
columnDefs = [
    {
        "headerName": "Gender", # Nom de la colonne
        "field": "Gender", # ID de la colonne (même nom que l'en-tête)
    },
    {
        "headerName": "Age", # Nom de la colonne
        "field": "Age", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Type numérique du filtre
    },
    {
        "headerName": "Money", # Nom de la colonne
        "field": "Money", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Type numérique du filtre
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
]

# Attributs de la table
defaultColDef = {
    "filter": True, # Filtre
    "floatingFilter": True, # Zone de saisie pour filtre
    "resizable": True, # Taille ajustable
    "sortable": True, # Trie
    "editable": True, # Données modifiables
    "minWidth": 100, # Taille mini par colonne
}

# Configuration de la table
table = dag.AgGrid(
    id="portfolio-table", # pour le callback
    className="ag-theme-alpine-dark", # Thème
    columnDefs=columnDefs, # voir config ci-avant
    rowData=None, # données vides
    columnSize="sizeToFit", # Colonnes ajustées à leurs largeurs
    defaultColDef=defaultColDef, # voir config ci-avant
)

# FRONT END ----------------------------------------------------------------

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Configuration de la page @
app.layout = dbc.Container(
    [   
        # Titre principal de la page @
        html.Div(
            "Investments Survey", # Texte
            className="h3 p-2 text-white bg-secondary", # Mise en forme
            id='not-important',
            ),
        
        dbc.Row(
            [
                dbc.Col(
                    [   
                        # Cartes : cadre
                        dbc.Card(
                            [   
                                # Cartes : en-tête
                                dbc.CardHeader(
                                    
                                    # Menu déroulant
                                    dcc.Dropdown(
                                        id='retrieve-dataset', # pour le callback
                                        options=datasets[0], # valeurs du menu
                                        value=datasets[0][0], # valeur affichée
                                        placeholder='Select dataset', # txt défaut
                                        clearable=False, # non supprimable
                                        style={'color':'black'}, # couleur texte
                                    ), 
                                    style={"width": "18rem"},
                                ),
                                
                                # Cartes : corps principapl
                                dbc.CardBody(
                                    [   
                                        # Table : configuration ci-avant
                                        table,
                                        
                                        dbc.Row([
                                            
                                           dbc.Col([
                                               
                                               # Zone de texte
                                               dbc.Input(
                                                   id="save-name", # callback
                                                   placeholder="Save as...", # survol
                                                   type="text", # type requis
                                                   value=None, # pas valeur affichée
                                                   className='mt-2' # espacement
                                               ),
                                           ], width=6),
                                           
                                            dbc.Col([
                                                
                                                # Bouton d'exécution
                                                dbc.Button(
                                                    id="save-btn", # callback
                                                    children="Save Table", # texte
                                                    color="primary", # couleur
                                                    size="md", # taille
                                                    className='mt-2'# espacement
                                                ),
                                            ], width=3)
                                        ]),
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=12,
                ),
            ],
            className="py-4",
        ),
        dbc.Row(
            
            # Message d'alerte
            dbc.Alert(children=None, # Pas de valeur au chargement page @
                      color="success", # Couleur de fonds
                      id='alerting', # pour le callback
                      is_open=False, # Pas d'affichage au chargement page @
                      duration=2_000, # Délai d'affichage
                      className='ms-4', # Marge
                      style={'width':'18rem'} # Mise en forme
            ),
        )
    ],
)

# INTERACTION DES COMPOSANTS ----------------------------------------------

# MAJ des données de la table à partir des données à partir de la valeur affichée
# au menu déroulant
@app.callback(
    Output("portfolio-table", # Sortie : table
           "rowData" # Fonctionnalité : données de la table
           ),
    Input("retrieve-dataset", "value"), # Entrée : menu déroulant
)
def update_portfolio_stats(dataset_selected):
    
    # print(dataset_selected)
    
    # Conversion du fichier .csv en DF pandas selon la valeur affichée du menu 
    # déroulant
    dff = pd.read_csv(f'data\\{dataset_selected}') 
    
    # MAJ des données de la table à partir des données de la DF ci-avant convertie
    # en dictionnaire
    return dff.to_dict('records')

# save your data
@app.callback(
    Output("alerting", # Sortie : message d'alerte
           "is_open", # Fonctionnalité : couleur
           ),
    Output("alerting", # Sortie : message d'alerte
           "children", # Fonctionnalité : texte
           ),
    Output("alerting", # Sortie : message d'alerte
           "color", # Fonctionnalité : couleur
           ),
    Input("save-btn", "n_clicks"), # Entrée : bouton d'exécution
    State("save-name", "value"), # State : zone de texte
    State("portfolio-table", "rowData"), # State : table
prevent_initial_call=True # pas de MAJ des composants lors du chargement page @
)
def update_portfolio_stats(n, name, data):

    # Si la table n'a aucune donnée
    if name is None or len(name)==0:
        
        # MAJ message d'alerte : Affichage, texte et couleur 
        return True, "Aucun nom de sauvegarde fournit", "danger"
    
    else:
        
        # Récupération des données de la table de type dict convertie en DF
        dff = pd.DataFrame(data)
        
        # Chargement de la DF selon le nom et le chemin suivant : 
        dff.to_csv(f'data\\{name}.csv', index=False)
        
        # MAJ du message d'alerte : Affichage, texte et couleur
        return True, "Fichier sauvegardé ! Well done!", "success"

if __name__ == "__main__":
    app.run_server(debug=True)
