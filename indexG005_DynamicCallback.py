"""
Lien : https://www.youtube.com/watch?v=4gDwKYaA6ww&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=6
Cours : Introduction to Dash Plotly Dynamic Callbacks

Documentation sur les callbacks dynamiques :
https://dash.plotly.com/pattern-matching-callbacks

Callbacks dynamiques = l'argument ID de chaque composant n'est plus un str mais
un dict

Ajout de plusieurs composants à chaque fois qu'on appuye sur le bouton d'exécution
Pour cela on a recours à des callbacks dynamiques, qui permettent, grâce à la
sous-librairie MATCH de dash, de distinguer l'ID de composants identiques et 
en utilisant une librairie pour l'argument 'id' de chaque composant.

Ce cours peut-être utile par exemple, pour afficher sur une même page @,
une table des flux commerciaux, une table des flux économiques, une table
des flux ...

MATCH : recoupement des n° index entrées et sorties
ALL : récupération pour le composant concerné de tous les index
ALLSMALLER : récupère tous les index saus le dernier index

Date : 16-11-2023
"""

from dash import (Dash, html, dcc, callback, Output, Input, State, 
                  ALLSMALLER, MATCH, ALL)
import plotly.express as px
import pandas as pd
import numpy as np

# BACK END --------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Caste.csv")

# Renommage des colonnes
df.rename(columns={'under_trial': 'under trial', 'state_name': 'state'}, 
          inplace=True)

# FRONT END -----------------------------------------------------------------

# Instanciation de la librairie Dash
app = Dash()

# Configuration de la page @
app.layout = html.Div([
    
    html.Div(children=[
        
        # Bouton d'exécution
        html.Button('Add Chart', # Texte affiché au bouton
                    id='add-chart', # pour le callback
                    n_clicks=0, # bouton non appuyé lors du chargement page @
                    ), 
    ]),
    
    # Zone vide
    html.Div(id='container', # pour le callback
             children=[], # zone vide
             )
])

# INTERACTION ENTRE LES COMPOSANTS -------------------------------------------

# Ajout des composants : graphique, bouton d'options, menus déroulants à chaque
# fois qu'on appuye sur le bouton d'exécution
@callback(
    Output('container', 'children'), # Sortie : zone vide
    [Input('add-chart', 'n_clicks')], # Entrée : bouton d'exécution
    [State('container', 'children')] # State : zone vide
)
def display_graphs(n_clicks, div_children):
    
    new_child = html.Div(
        
        # Mise en forme
        style={'width': '45%', 'display': 'inline-block', 
               'outline': 'thin lightgrey solid', 
               'padding': 10},
        
        # Composants de la page @
        children=[
            
            # Graphique (données vides)
            dcc.Graph(
                id={ # pour le callback
                    'type': 'dynamic-graph', # nom ID du composant
                    'index': n_clicks # l'index différencie du nom ID du composant
                },
                figure={}, # Données vides
            ),
            
            # Bouton d'options (choix du graphique)
            dcc.RadioItems(
                id={ # pour le callback
                    'type': 'dynamic-choice', # nom ID du composant
                    'index': n_clicks # l'index différencie du nom ID du composant
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'}, # valeurs
                         {'label': 'Line Chart', 'value': 'line'},
                         {'label': 'Pie Chart', 'value': 'pie'}],
                value='bar', # valeur affichée par défaut
            ),
            
            # Menu déroulant n° 1 (données du champ 'state' de la DF)
            dcc.Dropdown(
                id={ # pour le callback
                    'type': 'dynamic-dpn-s', # nom ID du composant
                    'index': n_clicks # l'index différencie du nom ID du composant
                },
                options=[{'label': s, 'value': s} # valeurs
                         for s in np.sort(df['state'].unique())],
                multi=True, # possibilité d'afficher plusieurs valeurs
                value=["Andhra Pradesh", # valeurs affichées par défaut
                       "Maharashtra"], 
            ),
            
            # Menu déroulant n° 2 (selon les champs 'caste', 'gender' et 'state')
            dcc.Dropdown(
                id={ # pour le callback
                    'type': 'dynamic-dpn-ctg', # nom ID du composant
                    'index': n_clicks # l'index différencie du nom ID du composant
                },
                options=[{'label': c, 'value': c} # valeurs
                         for c in ['caste', 'gender', 'state']],
                value='state', # valeur affichée par défaut
                clearable=False, # pas de possib de suppr la valeur affichée
            ),
            
            # Menu déroulant n° 3 (selon les champs 'detenues', 'under trial',...)
            dcc.Dropdown(
                id={ # pour le callback
                    'type': 'dynamic-dpn-num', # nom ID du composant
                    'index': n_clicks # l'index différencie du nom ID du composant
                },
                options=[{'label': n, 'value': n} # valeurs
                         for n in ['detenues', 'under trial', 
                                   'convicts', 'others']],
                value='convicts', # valeur affichée par défaut
                clearable=False, # pas de possib de suppr la valeur affichée
            )
        ]
    )
    
    # Ajout des composants ci-avant à chaque fois qu'on appuie sur le bouton
    # d'exécution
    div_children.append(new_child)
    
    # MAJ de la page @
    return div_children

# MAJ du graphique selon les données des 3 menus déroulants et du type de graphique
# à afficher selon l'option choisi dans le composant menu d'options
@callback(
    Output(component_id={ # Sortie : graphique
        'type': 'dynamic-graph', # nom de l'ID du composant
        'index': MATCH, # Recoupement index des entrées / index de la sortie
                         }, 
           component_property='figure',
           ),
    [Input(component_id={ # Entrée : menu déroulant n° 1
        'type': 'dynamic-dpn-s', # nom de l'ID du composant
        'index': MATCH, # Recoupement index des entrées / index de la sortie
                         }, 
           component_property='value',
           ),
     Input(component_id={ # Entrée : menu déroulant n° 2
         'type': 'dynamic-dpn-ctg', # nom de l'ID du composant
         'index': MATCH, # Recoupement index des entrées / index de la sortie
                         }, 
           component_property='value',
           ),
     Input(component_id={ # Entrée : menu déroulant n° 3
         'type': 'dynamic-dpn-num', # nom de l'ID du composant
         'index': MATCH, # Recoupement index des entrées / index de la sortie
                         }, 
           component_property='value',
           ),
     Input(component_id={ # Entrée : bouton d'options 
         'type': 'dynamic-choice', # nom de l'ID du composant
         'index': MATCH, # Recoupement index des entrées / index de la sortie
                         }, 
           component_property='value',
           )]
)
def update_graph(s_value, ctg_value, num_value, chart_choice):
    
    print(s_value)
    
    # Recoupement de la DF selon la valeur sélectionnée dans le menu déroulant n° 1
    dff = df[df['state'].isin(s_value)]

    # Si le diagramme en barres a été sélectionnée dans le composant boutons d'opt°
    if chart_choice == 'bar':
        
        # Regroupement des données de la DF selon la valeur affichée au menu
        # déroulant n° 2
        dff = dff.groupby([ctg_value], as_index=False)[[
            'detenues', 'under trial', 'convicts', 'others']].sum()
        
        # Configuration du diagramme en barres
        fig = px.bar(dff, # DF regroupée ci-avant
                     x=ctg_value, # axe des abscisses : données menu déroulant n° 2
                     y=num_value, # axe des ordonnées : données menu déroulant n° 3
                     )
        
        # MAJ du diagramme en barres
        return fig
    
    # Si le diagramme linéaire a été sélectionnée dans le composant boutons d'opt°
    elif chart_choice == 'line':
        
        # S'il n'y aucune valeur affichée au menu déroulant n° 1
        if len(s_value) == 0:
            
            # pas de graphique à afficher
            return {}
        
        else:
            
            # Regroupement des données de la DF selon la donnée affichée du menu
            # déroulant n° 2
            dff = dff.groupby([ctg_value, 'year'], as_index=False)[[
                'detenues', 'under trial', 'convicts', 'others']].sum()
            
            # Configuration du diagramme linéaire
            fig = px.line(
                dff, # DF regroupée ci-avant
                x='year', # Axe des abscissses
                y=num_value, # Axe des ordonnées
                color=ctg_value, # Donnée affichée du menu déroulant n° 2
                )
            
            # MAJ du diagramme circulaire
            return fig
    
    # Si le diagramme circulaire a été sélectionné dans le composant boutons d'opt°
    elif chart_choice == 'pie':
        
        # Configuration du diagramme circulaire
        fig = px.pie(dff, # DF
                     names=ctg_value, # Données du menu déroulant n° 2
                     values=num_value, # Données du menu déroulant n° 3
                     )
        
        # MAJ du diagramme circulaire
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
