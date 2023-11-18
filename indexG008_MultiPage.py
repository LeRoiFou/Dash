"""
Lien : https://dash.plotly.com/urls#dash-pages
Cours : https://dash.plotly.com/urls#dash-pages

Autre mise en forme avec des multi-pages.
En complément, on peut adapter la taille des colonnes selon la taille appliquée
à la fenêtre principale

Date : 18-11-2023
"""

from dash import Dash, html, page_registry, page_container
import dash_bootstrap_components as dbc

# Instanciation de la librairie et mise en page @
app = Dash(use_pages=True, 
           external_stylesheets=[dbc.themes.SPACELAB]
           )

# Configuration de la barre latérale
sidebar = dbc.Nav(
            [   
                # Liens
                dbc.NavLink(
                    [
                        html.Div(page["name"], # nom de l'onglet
                                 className="ms-2" # marges
                                 ),
                    ],
                    href=page["path"], # Référence de l'onglet
                    active="exact", # onglet sélectionné surligné
                )
                for page in page_registry.values() # pour chaque onglets
            ],
            vertical=True, # Vertical
            pills=True, # True : onglet sélectionné surligné
            className="bg-light", # couleur de fond
)

# Configuration de la page @
app.layout = dbc.Container([
    dbc.Row([
        
        dbc.Col(
            
            # Titre principal de la page @
            html.Div("Python Multipage App with Dash", # Texte
                     style={'fontSize':50, 'textAlign':'center'}, # Mise en forme
                     ))
    ]),

    # Ligne séparatrice
    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [   
                    # Barre latérale configurée ci-avant
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2,
                # xs (x small), sm (small medium)... adaptation de la taille
                # de cette colonne selon la taille de la fenêtre principale
                ), 

            dbc.Col(
                [   # Onglets à afficher
                    page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)
