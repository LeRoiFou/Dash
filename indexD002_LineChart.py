"""
Lien : https://www.youtube.com/watch?v=G8r2BB3GFVY&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=2
Cours : All about the Graph Component - Python Dash Plotly

Documentation dcc.Graph : 
https://dash.plotly.com/dash-core-components/graph

Cours sur les attributs attachés à un composant : graphique linéaire

Date : 12-10-23
"""

from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px

# Récupération de la DF
df = px.data.gapminder()

# FRONT END ---------------------------------------------------------------------

# Mise en page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la sous-librairie Dash
app = Dash(__name__, 
           external_stylesheets=external_stylesheets,
           )

# Configuration de la page @
app.layout = html.Div([
    
    # Menu déroulant
    dcc.Dropdown(id='dpdn2', # pour le callback
                 value=['Germany','Brazil'], # valeurs d'affichage par défaut
                 multi=True, # affichage multiple
                 options=[{'label': x, 'value': x} # valeurs du composant
                          for x in df.country.unique()], # par pays de la DF
                 ),
    
    html.Div([
        
        # Graphique n° 1 vide
        dcc.Graph(id='pie-graph', # pour le callback
                  figure={}, # valeurs vides
                  className='six columns', # largeur du graphique
                  ),
        
        # Graphique n° 2 vide
        dcc.Graph(id='my-graph', # pour le callback
                  figure={}, # valeurs vides
                  clickData=None, 
                  hoverData=None, # I assigned None for tutorial purposes. By default, these are None, unless you specify otherwise.
                  config={
                      'staticPlot': False, # True : graphique immobile
                      'scrollZoom': True, # zoom avec la roulette de la souris
                      'doubleClick': 'reset', # Réinitialisation
                      # Arguments pour doubleClick :
                      # 'reset' ou 'autosize' ou 'reset+autosize' ou 'False'
                      'showTips': False, # True : info double click réinitialisation
                      'displayModeBar': True, # Affichage du menu des boutons
                      # Arguments pour displayModeBar : True, False, 'hover'
                      'watermark': True, # Icône Plotly
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                      # modeBarButtonsToRemove : Boutons à supprimer du menu
                        },
                  className='six columns', # largeur du graphique
                  )
    ])
])

# INTERACTION DES COMPOSANTS ----------------------------------------------------

# MAJ du graphique en lignes selon la/les valeur(s) sélectionnée(s) dans le menu
# déroulant
@callback(
    Output(component_id='my-graph', # Sortie : graphique n° 2
           component_property='figure'),
    Input(component_id='dpdn2', # Entrée : menu déroulant
          component_property='value'),
)
def update_graph(country_chosen):
    
    # Recoupement sur la DF à partir d'un champ (valeur du menu déroulant) :
    # selon le pays sélectionné
    dff = df[df.country.isin(country_chosen)]
    
    # MAJ du graphique en ligne
    fig = px.line(
        data_frame=dff, # DF filtrée
        x='year', # axe des abscisses
        y='gdpPercap', # axe des ordonnées
        color='country', # couleur par pays
        custom_data=['country', 'continent', 'lifeExp', 'pop'],
        # custom_data : données à restituer en sélectionnant l'icône 
        # "Lasso select" du menu en haut du graphique
        )
    fig.update_traces(mode='lines+markers') # lignes avec points sur graphique
    
    return fig

#
@callback(
    Output(component_id='pie-graph', # Sortie : graphique n° 1 (camembert)
           component_property='figure'),
    Input(
        component_id='my-graph', # Entrée : graphique n° 2 (graphique en ligne)
        component_property='hoverData'), # fonction : survol sur le graph
    Input(
        component_id='my-graph', # Entrée : graphique n° 2 (graphique en ligne)
        component_property='clickData'), # fonction : clique sur le graph
    Input(
        component_id='my-graph', # Entrée : graphique n° 2 (graphique en ligne)
        component_property='selectedData'), # fonction : Box Select
    Input(
        component_id='dpdn2', # Entrée : menu déroulant
        component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    
    # S'il n'y a pas de survol des données (lors du chargement on ne survole
    # pas les données du graphique en ligne)
    if hov_data is None:
        
        # Recoupement sur la DF à partir d'un champ (valeur du menu déroulant)
        dff2 = df[df.country.isin(country_chosen)]
        
        # Filtre de la DF sur une année
        dff2 = dff2[dff2.year == 1952]
        
        # MAJ du camembert
        fig2 = px.pie(
            data_frame=dff2, # DF filtrée
            values='pop', # affichage sur la population
            names='country', # légende
            title='Population for 1952', # titre
            )
        
        return fig2
    
    else:
        
        # Affichage dans le terminal des données du graphique linéaire
        # selon le survol effectué sur ce graphique avec la souris
        # print(f'hover data: {hov_data}')
        
        # Affichage dans le terminal du pays selon le survol effectué avec
        # la souris sur le graphique linéaire
        # print(hov_data['points'][0]['customdata'][0])
        
        # Affichage dans le terminal des données du graphique linéaire
        # selon le clique effectué sur ce graphique avec la souris
        # print(f'click data: {clk_data}')
        
        # Affichage dans le terminal des données du graphique linéaire
        # selon la sélection des valeurs effectuée avec l'icône Box Select
        # print(f'selected data: {slct_data}')
        
        # Recoupement sur la DF à partir d'un champ (valeur du menu déroulant)
        dff2 = df[df.country.isin(country_chosen)]
        
        # Récupération de l'année dans le graphique linéaire selon la sélection
        # effectuée avec la souris en survolant le point concerné
        hov_year = hov_data['points'][0]['x']
        
        # Filtre de la DF selon l'année sélectionnée ci-avant
        dff2 = dff2[dff2.year == hov_year]
        
        # MAJ du camembert en fonction de l'année sélectionnée sur le graphique
        # linéaire
        fig2 = px.pie(
            data_frame=dff2, # DF filtrée
            values='pop', # affichage sur la population
            names='country', # légende
            title=f'Population for: {hov_year}') # titre
        
        return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
