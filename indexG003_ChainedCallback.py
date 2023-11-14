"""
Lien : https://www.youtube.com/watch?v=ZxshFO0bbZM&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=4
Cours : Chained Callback in Dash

Documentation sur les callback :
https://dash.plotly.com/basic-callbacks

Documentation sur les nuages de points :
https://plotly.com/python-api-reference/generated/plotly.express.scatter.html

# Enchaînement de callback : tant que le menu déroulant n° 2 n'est pas alimenté
par le menu déroulant n° 1, alors le graphique de nuage de points ne s'affiche pas

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
app = Dash(external_stylesheets=external_stylesheets,)

# Configuration de la page @
app.layout = html.Div([
    
    # Texte rattaché au menu déroulant n° 1
    html.Label(
        "State:", # Titre
        style={'fontSize':30, 'textAlign':'center'}, # Mise en forme
        ),
    
    # Menu déroulant n° 1
    dcc.Dropdown(
        id='states-dpdn', # pour le callback
        options=[{'label': s, 'value': s} # Valeurs du menu déroulant
                 for s in sorted(df.State.unique())],
        value=None, # Pas de valeurs affichées par défaut
        clearable=False # Valeurs affichées non effaçables
    ),
    
    # Texte rattaché au menu déroulant n° 2
    html.Label("Counties:", # Titre
               style={'fontSize':30, 'textAlign':'center'}, # Mise en forme
               ),
    
    # Menu déroulant n° 2 (données vides)
    dcc.Dropdown(
        id='counties-dpdn', # pour le callback
        options=[], # données vides
        value=[], # pas de valeurs affichées par défaut
        multi=True, # possibilité d'afficher plusieurs valeurs
        ),
    
    # Zone vide (pour le graphique)
    html.Div(id='graph-container', # pour le callback
             children=[], # données vides
             )
])

# INTERACTION DES COMPOSANTS ---------------------------------------------

# MAJ du menu déroulant n° 2 sur les valeurs contenues et les valeurs affichées 
# selon la valeur affichée dans le menu déroulant n° 1
@callback(
    Output('counties-dpdn', # Sortie : menu déroulant n° 2
           'options'), # Fonctionnalité : valeurs du menu déroulant
    Output('counties-dpdn', # Sortie : menu déroulant n° 2
           'value'), # Fonctionnalité : valeurs affichées par défaut
    Input('states-dpdn', 'value'), # Entrée : menu déroulant n° 1
)
def set_cities_options(chosen_state):
    
    # Filtre de la DF selon la valeur choisie dans le menu déroulant n° 1
    dff = df[df.State==chosen_state]
    
    # Alimentation des valeurs du menu déroulant n° 2 selon la valeur sélectionnée
    # dans le menu déroulant n° 1
    counties_of_states = [{'label': c, 'value': c} 
                          for c in sorted(dff.County.unique())]
    
    # Affichage des valeurs du menu déroulant n° 2 selon la valeur sélectionnée
    # dans le menu déroulant n° 1
    values_selected = [x['value'] for x in counties_of_states]
    
    # MAJ du menu déroulant n° 2 sur les valeurs contenues et les valeurs affichées
    return counties_of_states, values_selected


# MAJ du graphique nuage de points selon les valeurs affichées dans les menus
# déroulants n° 1 et n° 2
@callback(
    Output('graph-container', 'children'), # Sortie : graphique
    Input('counties-dpdn', 'value'), # Entrée : Menu déroulant n° 2
    Input('states-dpdn', 'value'), # Entrée: Menu déroulant n° 1
    prevent_initial_call=True # pas de MAJ lors du chargement de la page @
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
        dff = df[(df.State==selected_state) & 
                 (df.County.isin(selected_counties))]

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
        return dcc.Graph(id='display-map', # ID du composant
                         figure=fig, # Données configurées ci-avant
                         )


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
