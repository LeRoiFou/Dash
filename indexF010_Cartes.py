"""
Lien : https://www.youtube.com/watch?v=THB9AEwdSXo&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=11
Cours : Dash Bootstrap Card - the Advanced Stuff

Documentation sur les cartes :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/

Icônes pour les composants dbc : 
https://icons.getbootstrap.com/

KPI :
https://github.com/DashBookProject/Plotly-Dash/blob/master/Bonus-Content/Components/cards.md

Documentation sur Cheat Sheet : 
https://dashcheatsheet.pythonanywhere.com/

Configuration des cartes dont couleur des textes, alignement, espacement...

Date : 07-11-2023
"""

from dash import Dash, html
import dash_bootstrap_components as dbc

# CONFIGURATION DES COMPOSANTS ----------------------------------------------

# MINIMAL DASH BOOTSTRAP CARD--------------------------------------
        
        # Cartes : cadre
# card =  dbc.Card(
    
#     # Cartes
#     dbc.CardBody(
#         [   
#             # Titre H1
#             html.H1("Sales"),
            
#             # Titre H3
#             html.H3("$104.2M")
#         ],
#     ),
# )

# STYLING THE CARD (adding color and centering text)------------------------------

        # Cartes : cadre
# card =  dbc.Card(
    
#     # Cartes
#     dbc.CardBody(
#         [   
#             # Titre H1
#             html.H1("Sales"),
            
#             # Titre H3
#             html.H3("$104.2M", className="text-success") # success : couleur
#         ],
#     ),
#     className="text-center" # Texte centré
# )


# CARD WITH ICONS (adding icon and background color)-------------------------------------------------------------------

       # Cartes : cadre
card = dbc.Card(
    
    # Cartes
    dbc.CardBody(
        [   
            # Titre H1
            html.H1(children=[
                
                # Icône à insérer
                html.I(className="bi bi-bank me-2"), # Icône + espacement
                "Profit", # Texte
                ]),
            
            # Titre H3
            html.H3("$8.3M"),
            
            # Titre H4
            html.H4(
                
                # Icône à insérer
                html.I(
                    "10.3% vs LY", # Titre
                    className="bi bi-caret-up-fill text-success",# Icône + couleur   
                       )),
        ],
    ),
    className="text-center m-4 bg-primary text-white", 
    # alignement, espacement, couleur de fond et couleur de texte
)

# FRONT END ----------------------------------------------------------------

# Instanciation de la librairie et mise en page @
app = Dash(external_stylesheets=[
    dbc.themes.SPACELAB, # Thème
    dbc.icons.BOOTSTRAP, # Pour les icônes à insérer
    ])

# Configuration de la page @
app.layout=dbc.Container(card)


if __name__ == "__main__":
    app.run_server(debug=True)
