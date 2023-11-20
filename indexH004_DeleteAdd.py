"""
Lien : https://www.youtube.com/watch?v=LNQhY8NZmCY&list=PLh3I780jNsiRZX9Yciw-OupsNDeByUBhZ&index=2
Cours : Dash AG Grid - Delete and Add Buttons

Dans ce cours on apprend à supprimer / à ajouter une ligne de la table et 
de mettre à jour le graphique

Recours à une nouvelle sous-librairie de Dash : ctx (callback context)
cette librairie permet de récupérer l'identifiant d'un composant

Date : 20-11-2023
"""
import dash_ag_grid as dag      
from dash import Dash, html, dcc, callback, Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
import pandas as pd         
import plotly.express as px

# BACK END --------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/finance_survey.csv")

# Configuration des colonnes de la table
columnDefs = [
    {
        "headerName": "Gender", # Nom de la colonne
        "field": "Gender", # ID de la colonne (même nom que l'en-tête)
        "rowDrag": True, # Déplacement de la ligne
    },
    {
        "headerName": "Age", # Nom de la colonne
        "field": "Age", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Filtre numérique
    },
    {
        "headerName": "Money", # Nom de la colonne
        "field": "Money", # ID de la colonne (même nom que l'en-tête)
        "type": "rightAligned", # Alignement à droite
        "filter": "agNumberColumnFilter", # Filtre numérique
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

# Configuration des attributs de la table
defaultColDef = {
    "filter": True, # Filtre
    "floatingFilter": True, # Zone de saisie pour filtre
    "resizable": True, # Taille ajustable
    "sortable": True, # Trie
    "editable": True, # Données modifiables
    "minWidth": 150, # Taille mini par colonne
}

# Configuration de la table
table = dag.AgGrid(
    id="portfolio-table", # pour le callback
    className="ag-theme-alpine-dark", # thème
    columnDefs=columnDefs, # configuration des colonnes effectuée ci-avant
    rowData=df.to_dict("records"), # données de la table (DF convertie en dict)
    columnSize="sizeToFit", # Colonnes ajusées à leurs largeurs
    defaultColDef=defaultColDef, # attributs de la table configurés ci-avant
)

# FRONT END -------------------------------------------------------------------

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Configuration de la page @
app.layout = dbc.Container(
    [
        # Titre principal de la page @
        html.Div("Investments Survey", 
                 className="h3 p-2 text-white bg-secondary"),
        
        dbc.Row(
            [
                dbc.Col(
                    [   
                        # Cartes : cadre
                        dbc.Card(
                            [
                                # Cartes : corps de texte
                                dbc.CardBody(
                                    [   
                                        # Table configurée ci-avant
                                        table,
                                        
                                        html.Span(
                                            [   
                                                # Bouton d'exécution n° 1
                                                dbc.Button(
                                                    id="delete-row-btn", # callback
                                                    children="Delete row", # texte
                                                    color="secondary", # couleur
                                                    size="md", # taille
                                                    className='mt-3 me-1' # marges
                                                ),
                                                
                                                # Bouton d'exécution n° 2
                                                dbc.Button(
                                                    id="add-row-btn", # callback
                                                    children="Add row", # texte
                                                    color="primary", # couleur
                                                    size="md", # taille
                                                    className='mt-3' # marges
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=7,
                ),
                dbc.Col(
                    [   
                        # Cartes : cadre
                        dbc.Card(
                            [   
                                # Cartes : corps de texte
                                dbc.CardBody(
                                    [   
                                        # Zone vide (pour le graphique)
                                        html.Div(
                                            id="pie-breakdown", # callback
                                            className="card-text"
                                        )
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=5,
                ),
            ],
            className="py-4",
        ),
    ],
)

# INTERACTION DES COMPOSANTS -------------------------------------------------

# MAJ de la table selon le bouton d'exécution appuyé :
# -> Bouton d'exécution n° 1 : données à supprimer à la table
# -> Bouton d'exécution n° 2 : données à ajouter à la table
@callback(
    Output("portfolio-table", # Sortie : table
           "deleteSelectedRows"), # Fonctionnalités : données à supprimer
    Output("portfolio-table", # Sortie : table
           "rowData"), # Fonctionnalités : données de la table
    Input("delete-row-btn", "n_clicks"), # Entrée : Bouton d'exécution n° 1
    Input("add-row-btn", "n_clicks"), # Entrée : Bouton d'exécution n°  2
    State("portfolio-table", # State : table
          "rowData"), # Fonctionnalités : données de la table
    prevent_initial_call=True,
)
def update_dash_table(n_dlt, n_add, data):
    
    # Si l'ID du composant est "add-row-btn"...
    if ctx.triggered_id == "add-row-btn":
        
        # Assignation d'un dict pour alimenter la nouvelle DF ci-après
        new_row = {
            "Gender": [""],
            "Age": [0],
            "Money": [0],
            "Stock_Market": [""],
            "Objective": [""],
            "Source": [""]
        }
        
        # Nouvelle DF récupérant les données ci-avant
        df_new_row = pd.DataFrame(new_row)
        
        # Concaténation de la DF ci-avant avec la DF d'origine
        updated_table = pd.concat([pd.DataFrame(data), df_new_row])
        
        # MAJ de la table : pas de données à supprimer, et ajout de nouvelles données
        # dans cette table
        return False, updated_table.to_dict("records")

    # Si l'ID du composant est "delete-row-btn"
    elif ctx.triggered_id == "delete-row-btn":
        
        # MAJ de la table : données à supprimer, et pas d'ajout de nouvelles données
        # dans cette table
        return True, no_update

# MAJ du diagramme circulaire selon les données alimentées de la table et
# éventuellement modifiée
@callback(
    Output("pie-breakdown", "children"), # Sortie : graphique
    Input("portfolio-table", # Entrée : table
          "cellValueChanged"), # Fonctionnalité : valeur changée
    Input("portfolio-table", # Entrée : table
          "rowData"), # Fonctionnalité : données de la table
)
def update_portfolio_stats(cell_change, data):
    
    # Nouvelle DF selon les données de la table
    dff = pd.DataFrame(data)
    
    # MAJ et configuration du graphique : diagramme circulaire (camembert)
    return dcc.Graph(figure=px.pie(
        dff, # DF traitée ci-avant
        values='Money', # Valeurs du diagramme
        names='Source', # titre du graphique
        hole=0.3, # largeur du trou au centre du diagramme
        template="plotly_dark", # couleur de fond 
    ))


if __name__ == "__main__":
    app.run_server(debug=True)
