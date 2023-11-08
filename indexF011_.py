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

Bordure, icônes, marges et couleurs des cartes

Date : 07-11-2023
"""

from dash import Dash, html
import dash_bootstrap_components as dbc


# CONFIGURATION DES COMPOSANTS -------------------------------------------

# Cartes : cadre
card_sales = dbc.Card(
    
    # Carte
    dbc.CardBody(
        [   
            # Titre HI
            html.H1([
                
                # Icône à insérer
                html.I(className="bi bi-currency-dollar me-2"), # icône + marge
                "Sales", # Texte
                ], className="text-nowrap"),
            
            # Titre H3
            html.H3("$106.7M"),
           
            html.Div(
                [   
                    # Icône à insérer
                    html.I(
                        "5.8%", # Texte
                        className="bi bi-caret-up-fill text-success",
                        # icône + couleur
                        ),
                    " vs LY", # Texte
                ]
            ),
        ], 
        className="border-start border-success border-5"
        # couleur côté gauche et épaisseur bordure
        
    ),
    className="text-center m-4" # alignement et marge
)

# Cartes : cadre
card_profit = dbc.Card(
    
    # Carte
    dbc.CardBody(
        [   
            # Titre H1
            html.H1([
                
                # Icône à insérer
                html.I(className="bi bi-bank me-2"), # Icône + marge
                     "Profit", # Texte
                     ], 
                    className="text-nowrap"),
            
            # Titre H3
            html.H3("$8.3M",),
            
            html.Div(
                [   
                    # Icône à insérer
                    html.I("12.3%", # Texte
                           className="bi bi-caret-down-fill text-danger",
                           # icône et couleur
                           ),
                    " vs LY", # Texte
                ]
            ),
        ], className="border-start border-danger border-5"
        # couleur côté gauche et épaisseur bordure
    ),
    className="text-center m-4", # alignement et marge
)

# Cartes : cadre
card_orders = dbc.Card(
    
    # Carte
    dbc.CardBody(
        [   
            # Titre H1
            html.H1([
                
                # Icône à insérer
                html.I(className="bi bi-cart me-2"), # icône + marge
                     "Orders", # texte
                     ], className="text-nowrap"),
            
            # Titre H3
            html.H3("91.4K"),
            
            html.Div(
                [
                    html.I(
                        "10.3%", # Texte
                        className="bi bi-caret-up-fill text-success"
                        # icône + couleur
                        ),

                    " vs LY", # Texte
                ]
            ),
        ], className="border-start border-success border-5"
        # couleur côté gauche et épaisseur bordure
    ),
    
    className="text-center m-4",
    # Alignement et marge
)

# FRONT END ----------------------------------------------------------------

# Instanciation de la librairie et mise en page @
app = Dash(external_stylesheets=[dbc.themes.SPACELAB, # Thème
                                 dbc.icons.BOOTSTRAP, # Pour les icônes à insérer
                                 ])

# Configuration de la page @
app.layout = dbc.Container(
    dbc.Row(
        [dbc.Col(card_sales), 
         dbc.Col(card_profit), 
         dbc.Col(card_orders)],
    ),
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
