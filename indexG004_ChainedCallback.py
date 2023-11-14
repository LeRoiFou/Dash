"""
Lien : https://www.youtube.com/watch?v=ZxshFO0bbZM&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=4
Cours : Chained Callback in Dash

Documentation sur les callback :
https://dash.plotly.com/basic-callbacks

Documentation sur les nuages de points :
https://plotly.com/python-api-reference/generated/plotly.express.scatter.html

À la différence du précédent script, cette fois-ci il n'y a qu'une seule sortie
pour le 1er callback, qui va par la suite générer un callback supplémentaire

Date : 14-11-2023
"""

from dash import Dash, html, dcc, callback, Output, Input, no_update
import pandas as pd
import plotly.express as px
# need to pip install statsmodels for trendline='ols' in scatter plot

# BACK END ------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/social-capital-project.csv")

# FRONT END ----------------------------------------------------------

# Mise en page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div([
    
    # Texte rattaché au menu déroulant n° 1
    html.Label("State:", # Titre
               style={'fontSize':30, 'textAlign':'center'}, # Mise en forme
               ),
    
    # Menu déroulant n° 1
    dcc.Dropdown(
        id='states-dpdn', # pour le callback
        options=[{'label': s, 'value': s} # Valeurs du menu déroulant
                 for s in sorted(df.State.unique())],
        value='Alaska', # Valeur affichée par défaut
        clearable=False, # Valeurs affichées non effaçables
    ),

    # Texte rattaché au menu déroulant n° 2
    html.Label(
        "Counties:", # Titre
        style={'fontSize':30, 'textAlign':'center'}, # Mise en forme
        ),
    
    # Menu déroulant n° 2 (données vides)
    dcc.Dropdown(
        id='counties-dpdn', # pour le callback
        options=[], # données vides
        multi=True, # possibilité d'afficher plusieurs valeurs
        ),

    # Graphique (données vides)
    dcc.Graph(id='display-map', # pour le callback
              figure={}, # Données vides
              )
])

# INTERACTION DES COMPOSANTS ---------------------------------------------

# MAJ du menu déroulant n° 2 selon la valeur affichée au menu déroulant n° 1
callback(
    Output('counties-dpdn', 'options'), # Sortie : menu déroulant n° 2
    Input('states-dpdn', 'value') # Entrée : menu déroulant n° 1
)
def set_cities_options(chosen_state):
    
    # Filtre de la DF selon la valeur affichée au menu déroulant n° 1
    dff = df[df.State==chosen_state]
    
    # Alimentation des valeurs du menu déroulant n° 2 selon la DF filtrée ci-avant
    return [{'label': c, 'value': c} for c in sorted(dff.County.unique())]

# MAJ des valeurs affichées du menu déroulant n° 2 selon les valeurs contenues dans
# ce même composant
callback(
    Output('counties-dpdn', # Sortie : menu déroulant n° 2
           'value'), # Focntionnalité : valeurs affichées
    Input('counties-dpdn', # Entrée : menu déroulant n° 2
          'options') # Fonctionnalité : valeurs contenues
)
def set_cities_value(available_options):
    
    # MAJ des valeurs affichées en fonction des valeurs contenues dans le menu
    # déroulant n° 2
    return [x['value'] for x in available_options]

# MAJ du graphique nuage de points selon les valeurs affichées dans les menus
# déroulants n° 1 et n° 2
callback(
    Output('display-map', 'figure'), # Sortie : graphique
    Input('counties-dpdn', 'value'), # Entrée : Menu déroulant n° 2
    Input('states-dpdn', 'value') # Entrée: Menu déroulant n° 1
)
def update_grpah(selected_counties, selected_state):
    
    # Si aucune valeur n'est affichée dans le menu déroulant n° 2
    if len(selected_counties) == 0:
        
        # Pas de MAJ
        return no_update
    
    # Si au moins une valeur est affichée dans le menu déroulant n° 2
    else:
        
        # Filtre de la DF selon la valeur affichée dans le menu déroulant n° 1
        # et recoupement avec les valeurs affichées dans le menu n° 2
        dff = df[(df.State==selected_state) & (df.County.isin(selected_counties))]

        # Configuration du graphique : nuage de points
        fig = px.scatter(
            dff, # DF filtrée et recoupée ci-avant
            x='% without health insurance', # Données axe des abscisses
            y='% in fair or poor health', # Données axe des ordonnées
            color='% adults graduated high school', # Couleur des bulles
            trendline='ols', # affichage de la courbe tendance
            size='bubble_size', # Taille des bulles neutres
            hover_name='County', # Survol : Titre info-bulle
            # hover_data={'bubble_size':False}, # Survol : taille des bulles
            labels={'% adults graduated high school':'% graduated high school',
                    '% without health insurance':'% no health insurance',
                    '% in fair or poor health':'% poor health'},
            # labels : survol -> données affichées avec les valeurs
            )
        
        # MAJ du graphique - nuage de points
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
