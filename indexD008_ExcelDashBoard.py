"""
Lien : https://www.youtube.com/watch?v=acFOhdo_bxw&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=10
Cours : How to build Interactive Excel Dashboard with Python - Dash

MAJ du du diagramme en barres selon la valeur choisie dans le menu déroulant

Date : 19-10-23
"""

from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

# DS ------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/vgsales.csv")

# # Affichage des 5 premières lignes
# print(df.head())

# Affichage des champs composants n° 2, 3,... des 5 premières lignes
# print(df.iloc[:5, [2,3,5,10]])

# Affichage d'un entier : nombre de valeurs uniques (comme pour PowerBI)
# print(df.Genre.nunique())

# Affichage des valeurs uniques
# print(df.Genre.unique())

# Trie par ordre croissant des années en valeurs uniques
# print(sorted(df.Year.unique()))

# CONFIGURATION DES COMPOSANTS ------------------------------------------------

# Camembert
fig_pie = px.pie(data_frame=df, # Données de la DF
                 names='Genre', # Légende 
                 values='Japan Sales', # Valeurs du composant
                 )

# Camembert
fig_pie = px.pie(data_frame=df, # Données de la DF
                 names='Genre', # Légende
                 values='North American Sales', # Valeurs du composant
                 )

fig_pie.show()

# Diagramme en barres
fig_bar = px.bar(data_frame=df, # Données de la DF
                 x='Genre', # Axe des abscisses
                 y='Japan Sales', # Axe des ordonnées
                 )
fig_bar.show()

# Histogramme
fig_hist = px.histogram(data_frame=df, # Données de la DF
                        x='Year', # Axe des abscisses
                        y='Japan Sales', # Axe des ordonnées
                        )

fig_hist.show()

# FRONT END ----------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout=html.Div([
    
    # Titre principal
    html.H1("Graph Analysis with Charming Data"),
    
    # Menu déroulant
    dcc.Dropdown(id='genre-choice', # pour le callback
                 options=[{'label':x, 'value':x} # valeurs du composant
                          for x in sorted(df.Genre.unique())],
                 value='Action', # affichage par défaut
                 ),
    
    # Graphique (vide)
    dcc.Graph(id='my-graph', # pour le callback
              figure={}, # données vides
              ),
])

# INTERACTION DES COMPOSANTS ---------------------------------------------------

# MAJ du du diagramme en barres selon la valeur choisie dans le menu déroulant
@callback(
    Output(component_id='my-graph', # Sortie : graphique
           component_property='figure'),
    Input(component_id='genre-choice', # Entrée : menu déroulant
          component_property='value')
)
def interactive_graphs(value_genre):
    
    print(value_genre)
    
    # Filtre opéré sur la DF selon la valeur choisie dans le menu déroulant
    dff = df[df.Genre==value_genre]
    
    # MAJ du diagramme en barres
    fig = px.bar(data_frame=dff, # DF filtrée
                 x='Year', # Axe des abscisses
                 y='Japan Sales', # Axe des ordonnées
                 )
    
    return fig


if __name__=='__main__':
    app.run_server(debug=True)
