"""
Lien : https://www.youtube.com/watch?v=qxyPrvaqm9g&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=11
Cours : Financial app - Dropdown w Candlestick & OHLC charts - Plotly Dash

Documentation sur Article Comparing Candlestick and OHLC : 
https://lessonsfinancial.com/2020/04/01/edu-campaign-five-candlestick-patterns-for-day-trading/

Documentation sur Plotly Candlestick docs:
https://plotly.com/python/candlestick-charts/

Documentation sur Plotly OHLC docs:
https://plotly.com/python/ohlc-charts/

Dans ce programme on visualise deux graphiques qui présente des valeurs selon
un ordre chronologique (axe des abscisses), qui sont similaires à des graphiques
linéaires, à différence que pour chaque valeur (journalière, hebdo...), il y a
une valeur minimum et une valeur maximum selon une présentation différente au
regard de l'un des graphiques présentés dans ce script.

Si la valeur (journalière, hebdo...) a augmenté en fin de journée, semaine... par
rapport à la valeur en début de journée, semaine... alors, la référence sur le 
graphique concerné sera de couleur verte, à l'inverse, la référence sera de
couleur rouge.

Date : 24-10-23
"""

from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# DS ----------------------------------------------------------------------

# Récupération du fichier .csv converti en DF Pandas
df = pd.read_csv('assets/oil_prices.csv')

# Convertion du champ en datetime
df.Date = pd.to_datetime(df.Date)

# FRONT END ------------------------------------------------------------

# Assignation de la librairie Dash
app = Dash(external_stylesheets=[dbc.themes.LUMEN])

# Configuration de la page @
app.layout = dbc.Container([
    
    # Titre principal de la page @
    html.H1('Candlestick vs OHLC Charts', 
            style={'textAlign': 'center'},
            ),

    dbc.Row([
        
        dbc.Col([
            
            # Titre rattaché à la zone de saisie
            html.Label('Volume of oil over:'),
            
            # Zone de saisie avec mini-menu déroulant
            dcc.Input(
                id='oil-volume', # pour le callback
                type='number', # obligatoire des chiffres à saisir
                min=80000, # valeur minimum
                max=700000, # valeur maximum
                step=10000, # échelle
                value=80000, # valeur de saisie affichée par défaut
                )
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            
            # Titre rattaché au premier graphique
            html.Label('CandleStick Chart')], width=dict(size=4, offset=2)),
        
        dbc.Col([
            
            # Titre rattaché au deuxième graphique
            html.Label('OHLC Chart')], width=dict(size=4, offset=2))
    ]),

    dbc.Row([
        
        dbc.Col([
            
            # 1er graphique (vide)
            dcc.Graph(
                id='candle', # pour le callback
                figure={}, # valeurs vides
                style={'height': '80vh'}, # hauteur du graphique
                )], width=6),
        
        dbc.Col([
            
            # 2ème graphique (vide)
            dcc.Graph(
                id='ohlc', # pour le callback
                figure={}, # valeurs vides
                style={'height': '80vh'}, # hauteur du graphique
                )], width=6)
    ]),
], fluid=True)

# INTERACTION DES COMPOSANTS -----------------------------------

# Selon la valeur saisie dans la zone de saisie, MAJ du graphique
@callback(
    Output(component_id='candle', # Sortie : 1er graphique
           component_property='figure'),
    Output(component_id='ohlc', # Sortie : 2ème graphique
           component_property='figure'),
    Input(component_id='oil-volume', # Entrée : zone de saisie
          component_property='value')
)
def build_graphs(chosen_volume): 
    
    # Filtre opéré sur la DF selon la valeur saisie dans la zone de saisie
    dff = df[df.Volume > chosen_volume]
    print(dff.head())

    # MAJ du 1er graphique
    fig_candle = go.Figure(
        go.Candlestick(x=dff['Date'], # axe des abscisses
                       open=dff['Open'], # Valeur d'ouverture
                       high=dff['High'], # Valeur journalière la + haute
                       low=dff['Low'], # Valeur journalière la + basse
                       close=dff['Close'], # Valeur de fermeture
                       text=dff['Volume'],
                       )
    )
    fig_candle.update_layout(
        margin=dict(t=30, b=30), # marges
        # xaxis_rangeslider_visible=False, # True : "sous-graphique" à enlever
        )  

    # MAJ du 2ème graphique
    fig_ohlc = go.Figure(
        go.Ohlc(x=dff['Date'], # axe des abscisses
                open=dff['Open'], # Valeur d'ouverture
                high=dff['High'], # Valeur journalière la + haute
                low=dff['Low'], # Valeur journalière la + basse
                close=dff['Close'], # Valeur de fermeture
                text=dff['Volume'],
                )
    )
    fig_ohlc.update_layout(margin=dict(t=30, b=30)) # marges
    
    return fig_candle, fig_ohlc


if __name__=='__main__':
    app.run_server(debug=True)
