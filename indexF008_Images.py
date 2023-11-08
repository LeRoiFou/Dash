"""
Lien : https://www.youtube.com/watch?v=THB9AEwdSXo&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=11
Cours : Dash Bootstrap Card - the Advanced Stuff

Documentation sur les cartes :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/

Icônes pour les composants dbc : 
https://icons.getbootstrap.com/

KPI :
https://github.com/DashBookProject/Plotly-Dash/blob/master/Bonus-Content/Components/cards.md

Dans ce fichier - insertion d'une image selon 3 possibilités avec mise en forme
de la carte : ombre, marge, couleur texte...

Date : 07-11-2023
"""

from dash import Dash, html
import dash_bootstrap_components as dbc

# CONFIGURATION DES COMPOSANTS ----------------------------------------

# URL de l'image à afficher
count = "https://user-images.githubusercontent.com/72614349/194616425-107a62f9-06b3-4b84-ac89-2c42e04c00ac.png"

# Carte avec image chargée d'une URL -------------------------------------
# card = dbc.Card([
    
#     # Carte - image 
#     dbc.CardImg(src=count, # chemin et nom de l'image chargée
#                 top=False, # Position de l'image par rapport à la carte
#                 ),
    
#     # Carte - corps de texte
#     dbc.CardBody(
#         [   
#             # Titre H3
#             html.H3("Count von Count", # Texte
#                     className="text-primary", # Couleur du texte
#                     ),
            
#             html.Div("Chief Financial Officer"),
            
#             html.Div("Sesame Street, Inc.", 
#                      className="small", # Taille du texte
#                      ),
#         ]
#     )],
#     className="shadow my-2", # ombre + marge
#     style={"maxWidth": 350}, # Taille max
# )


# Carte avec une image chargée d'un lien @ ---------------------------------------
# card = dbc.Card([
    
#     # Carte avec lien
#     dbc.CardLink(
#         [
#             dbc.CardImg(src=count, # chemin et nom de l'image chargée
#                         top=True, # Position de l'image par rapport à la carte
#                         )
#         ],
#         href="https://en.wikipedia.org/wiki/Count_von_Count" # Lien
#     ),
    
#     # Carte - corps de texte
#     dbc.CardBody(
#         [   
#             # Titre H3
#             html.H3(
#                 "Count von Count", # Texte
#                 className="text-primary", # Couleur du texte
#                 ),
            
#             html.Div("Chief Financial Officer"),
            
#             html.Div("Sesame Street, Inc.", 
#                      className="small", # Taille du texte
#                      ),
#         ]
#     )],
                
#     className="shadow my-2", # ombre + marge
#     style={"maxWidth": 350}, # Taille max
# )


# Image en fond de page @ -------------------------------------------------
card = dbc.Card([
    
    # Carte - image 
    dbc.CardImg(src=count, # chemin et nom de l'image chargée
                ),
    
    # Ajout de l'image dans le fond de la page @
    dbc.CardImgOverlay([
        
        # Carte - corps de texte
        dbc.CardBody(
            [   
                # Titre H3
                html.H3(
                    "Count von Count", # Texte
                    className="text-light text-center", # Couleur et alignement
                    )
            ],
            style={"marginTop":160}) # Marge haut max
    ])
],
    className="shadow my-2", # Ombre + marge
    style={"maxWidth": 350}, # Taille max
)

# FRONT END ----------------------------------------------------------

# Instanciation de la librairie et mise en page @
app = Dash(external_stylesheets=[dbc.themes.SPACELAB])

# Configuration de la page @
app.layout=dbc.Container(card)

if __name__ == "__main__":
    app.run_server(debug=True)