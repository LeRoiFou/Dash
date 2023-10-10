"""
Lien : https://www.youtube.com/watch?v=d9SmpNfMg7U&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=19
Cours : Use a Slider in a Python Data App - Dash Plotly

Documentation sur dcc.Slider :
https://dash.plotly.com/dash-core-components/slider

Documentation sur Plotly Dash Slider Components :
https://github.com/DashBookProject/Plotly-Dash/blob/master/Bonus-Content/Components/sliders.md

Etude sur le nombre de tempêtes violentes aux USA, et les coûts engendrés

Date : 10-10-23
"""

from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import math

# DS ------------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/severe-storms.csv")

# CONFIGURATION DES COMPOSANTS -------------------------------------------------

# Gradients pour la barre de défilement 2.0
rangeslider_marks = {0:'$0', 5:'$5 billion', 10:'$10 billion', 
                     15:'$15 billion', 20:'$20 billion',
                     25:'$25 billion', 30:'$30 billion', 
                     35:'$35 billion', 40:'$40 billion'}

# FRONT END -------------------------------------------------------------------s

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div(
    [
        # Titre principal
        html.H1("Severe Storms Analysis in the USA", 
                style={'textAlign': 'center'},
                ),

        # Label pour la barre de défilement 1.0
        html.Label("Number of Severe Storms"),
        
        # Barre de défilement 1.0 avec une valeur de début fixée
        dcc.Slider(min=df['Severe Storm Count'].min(), # valeur minimum
                   max=df['Severe Storm Count'].max(), # valeur maximum
                   step=1, # valeur d'écart par gradient
                   value=13, # valeur par défaut affiché
                   tooltip={"placement": "bottom", # info-bulles
                            "always_visible": True},
                   updatemode='drag', # enregistre la valeur sélectionnée (bind)
                   persistence=True, # Selon la sauvegarde ci-après
                   persistence_type='session', # 'memory' or 'local'
                   id="my-slider", # pour le callback
        ),

        # Label pour la barre de défilement 2.0
        html.Label("Severe Storm Costs ($ Billions)"),
        
        # Barre de défilement 2.0 avec valeur de début non fixée
        dcc.RangeSlider(min=df['Severe Storm Costs (Billions)'].min(), # min
                        max=math.ceil(
                            df['Severe Storm Costs (Billions)'].max()), # max
                        step=1, # valeur d'écart par gradient
                        marks=rangeslider_marks, # configuration composant
                        value=[0,10], # valeurs par défaut affichés
                        tooltip={"placement": "bottom", # info-bulles
                                 "always_visible": True},
                        updatemode='drag', # enregistre la valeur sélectionnée
                        id="my-rangeslider", # pour le callback
        ),

        # Graphique vide
        dcc.Graph(id='my-graph', # pour le callback
                  )
    ],
    style={"margin": 30}
)

# INTERACTION DES COMPOSANTS -------------------------------------------------------

# Données du diagramme en barres adaptées selon les les valeurs sélectionnées
# dans les barres de défilement
@callback(
    Output('my-graph', 'figure'), # Sortie : graphique
    Input('my-slider', 'value'), # Entrée : barre de défilement 1.0
    Input('my-rangeslider', 'value') # Entrée : barre de défilement 2.0
)
def update_graph(n_storms, dollar_range):
    
    print(f'Valeur sélectionné dans la barre de défilement 1.0 : {n_storms}')
    print(f'Type de valeur pour la barre de défilement 1.0 : {type(n_storms)}')
    print(f'Valeur sélectionné dans la barre de défilement 1.0 : {dollar_range}')
    print(f'Type de valeur pour la barre de défilement 1.0 : {type(dollar_range)}')
    
    # Filtre opéré sur la DF à partir de la barre de défilement 1.0 :
    # restitution des données en booléen
    bool_series = df['Severe Storm Count'].between(0, # valeur min
                                                   n_storms, # valeur max
                                                   inclusive='both',
                                                   )
    # Filtre sur les valeurs 'True' suite au traitement opéré ci-avant
    df_filtered = df[bool_series]
    
    # MAJ du graphique : diagramme en barres
    fig = px.bar(data_frame=df_filtered,
                 x='Year', # axe des abscisses
                 y='Severe Storm Count', # axe des ordonnées
                 range_y=[df['Severe Storm Count'].min(), # valeur min axe y
                          df['Severe Storm Count'].max()], # valeur max axe y
                 range_x=[df['Year'].min()-1, # valeur min axe x
                          df['Year'].max()+1], # valeur max axe y
                 )

    # Filtre opéré sur la DF à partir de la barre de défilement 2.0
    # restitution des données en booléen
    bool_series2 = df['Severe Storm Costs (Billions)'].between(
        dollar_range[0], # valeur min (1er composant de la liste)
        dollar_range[1], # valeur max (2ème composant de la liste)
        inclusive='both',
        )
    
    # Assignation en liste des années récupérées selon le filtre opéré ci-avant
    # en récupérant uniquement les valeur True
    filtered_year = df[bool_series2]['Year'].values
    
    # MAJ du graphique : couleurs attribuées selon la valeur sélectionnée
    # dans la barre de défilement 2.0
    fig["data"][0]["marker"]["color"] = [
        "orange" if c in filtered_year 
        else "blue" 
        for c in fig["data"][0]["x"]
        ]

    return fig

if __name__ == "__main__":
    app.run(debug=True)
