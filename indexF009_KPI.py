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

KPI avec MAJ des données avec la librairie requests

Date : 07-11-2023
"""

from dash import Dash, dcc, html, callback, Input, Output, no_update
import dash_bootstrap_components as dbc
import requests

# BACK END -----------------------------------------------------------------

# Assignation d'une liste des monnaies virtuelles
coins = ["bitcoin", "ethereum", "binancecoin", "ripple"]

# MAJ des données toutes les 6 secondes
interval = 6_000 

# URL API des crypto-monnaies
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"

# Récupération des valeurs des crypto-monnaies
def get_data():
    
    try:
        
        # Requête API pour récupérer les valeurs
        response = requests.get(api_url, timeout=1)
        
        # Transformation des données sous format JSON (dictionnaire)
        return response.json()
    
    # En cas d'erreur de récupération des données / de connection...
    except requests.exceptions.RequestException as e:
        
        print(e)


def make_card(coin):
    
    # Récupération de la valeur de cette clé du dictionnaire
    change = coin["price_change_percentage_24h"]
    
    # Récupération la valeur de cette clé du dictionnaire
    price = coin["current_price"]
    
    # Couleur selon la valeur de la clé price_change_percentage_24h
    color = "danger" if change < 0 else "success"
    
    # Icône à récupérer selon la valeur concernée (https://icons.getbootstrap.com/)
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"
    
    return dbc.Card(
        html.Div(
            [   
                # Titre H4
                html.H4(
                    [   
                        # Image
                        html.Img(
                            src=coin["image"], # chemin et nom de l'image
                            height=35, # Taille
                            className="me-1", # Marge
                            ),
                        
                        coin["name"], # Récupération de la valeur de la clé 'name'
                    ]
                ),
                
                # Titre H4
                html.H4(f"${price:,}"), # valeur récupérée
                
                # Titre H5
                html.H5(
                    [f"{round(change, 2)}%", # valeur récupérée
                     html.I(className=icon), # Icône à charger
                     " 24hr"],
                    className=f"text-{color}", # Couleur du texte
                ),
            ],
            
            className=f"border-{color} border-start border-5",
            # Couleur à gauche de la bordure et marge
        ),
        
        className="text-center text-nowrap my-2 p-2",
        # Alignement
    )

# CONFIGURATION DES COMPOSANTS ---------------------------------------------

# Lien
mention = html.A(
    "Data from CoinGecko", # Titre
    href="https://www.coingecko.com/en/api", # Lien
    className="small" # Taille du texte
)

# MAJ des données
interval = dcc.Interval(interval=interval)

# Zone vide pour les cartes
cards = html.Div()

# FRONT END -----------------------------------------------------------------

app = Dash(external_stylesheets=[dbc.themes.SUPERHERO, 
                                 dbc.icons.BOOTSTRAP,
                                 ])

app.layout = dbc.Container([interval, # MAJ des données
                            cards, # Cartes
                            mention, # Lien
                            ], className="my-5")

# INTERACTION DES COMPOSANTS --------------------------------------------

# 
@callback(Output(cards, "children"), # Sortie : cartes
          Input(interval, "n_intervals")) # Entrée : MAJ des données
def update_cards(_): 
    # Paramètre obligatoire en cas de recours du composant dcc.Interval()
    
    coin_data = get_data()
    
    if coin_data is None or type(coin_data) is dict:
        
        return no_update

    # Assignation d'une liste des cartes à afficher
    coin_cards = []
    
    updated = None
    
    for coin in coin_data:
        
        if coin["id"] in coins:
            
            print(coin)
            
            updated = coin.get("last_updated")
            
            coin_cards.append(make_card(coin))

    # make the card layout
    card_layout = [
        
        dbc.Row([dbc.Col(card, md=3) for card in coin_cards]),
        
        dbc.Row(dbc.Col(f"Last Updated {updated}")),
    ]
    
    return card_layout


if __name__ == "__main__":
    app.run_server(debug=True)
