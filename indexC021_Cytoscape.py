"""
Lien : https://www.youtube.com/watch?v=iuHFwHgQIwg&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=15
Cours : Dash Cytoscape - Styling

Documentation sur Cytoscape :
https://dash.plotly.com/cytoscape/reference

Documentation sur Cytoscape Styling :
https://dash.plotly.com/cytoscape/styling

Style : 'documentation/Cytoscape_Styling.docx

Le cytoscape est un composant atypique : il peut-être utilisé dans un 
organigramme d'un groupe à titre d'exemple, ou organigramme interne d'une entreprise

Pour ce composant, un noeud est appelé 'node' et un lien est appelé 'edge'

Date : 05-10-23
"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_cytoscape as cyto
import pandas as pd

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Cytoscape/org-data.csv")

# CONFIGURATION DES COMPOSANTS  --------------------------------------------------

# Éléments configurés pour le cytoscape
my_elements=[
    
    # Dictionnaire pour le noeud 'Executive Director (Harriet)'
    {'data': {'id': 'ed', 
              'label': 'Executive Director (Harriet)'},
     'classes': 'purple' # One class
     },
    
    # Dictionnaire pour le noeud 'Vice President (Sarah)'
    {'data': {'id': 'vp1', 
              'label': 'Vice President (Sarah)'},
     'classes': 'square' # One class
     },
    
    # Dictionnaire pour le noeud 'Vice President (Charlotte)'
    {'data': {'id': 'vp2', 
              'label': 'Vice President (Charlotte)'},
     'classes': 'square' # One class
     },
    
    # Dictionnaire pour le noeud 'Program Officer (Sojourner)'
    {'data': {'id': 'po1', 
              'label': 'Program Officer (Sojourner)'},
     'classes': 'green diamond'  # Multiple classes
     },
    
    # Dictionnaire pour le noeud 'Program Officer (Elizabeth)'
    {'data': {'id': 'po2', 
              'label': 'Program Officer (Elizabeth)'},
     'classes': 'green diamond ' # Multiple classes
     },
    
    # Dictionnaire pour le noeud 'Program Associate (Ellen)'
    {'data': {'id': 'pa', 
              'label': 'Program Associate (Ellen)'},
     'classes': 'myimage' # One class
     },

    # Lien entre le noeud 'Executive Director (Harriet)' et 
    # 'Vice President (Sarah)'
    {'data': {
        'source': 'ed', 'target': 'vp1', 
        'weight': 1}, # texte inséré dans le lien
     'classes': 'purple'},
    
    # Lien entre le noeud 'Executive Director (Harriet)' et 
    # 'Vice President (Charlotte)'
    {'data': {
        'source': 'ed', 'target': 'vp2', 
        'weight': 2}}, # texte inséré dans le lien
    
    # Lien entre le noeud 'Vice President (Sarah)' et
    # 'Program Officer (Sojourner)'
    {'data': {
        'source': 'vp1', 'target': 'po1', 
        'weight': 3}}, # texte inséré dans le lien
    
    # Lien entre le noeud 'Vice President (Sarah)' et
    # 'Program Officer (Elizabeth)'
    {'data': {
        'source': 'vp1', 'target': 'po2', 
        'weight': 4}}, # texte inséré dans le lien
    
    # Lien entre le noeud 'Vice President (Charlotte)' et
    # 'Program Associate (Ellen)'
    {'data': {
        'source': 'vp2', 'target': 'pa', 
        'weight': 5}} # texte inséré dans le lien
]

# FRONT END ------------------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Assignation de la sous-librairie Dash
app = Dash(__name__, 
           external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    html.Div([
        
        # Menu déroulant
        dcc.Dropdown(
            id='dpdn', # pour le callback
            value='breadthfirst', # valeur par défaut affichée
            clearable=False, # valeur affichée non supprimable
            options=[ # valeurs du menu déroulant
                {'label': name.capitalize(), 'value': name}
                for name in ['breadthfirst' ,'grid', 'random', 'circle', 
                             'cose', 'concentric']
            ]
        ),
        
        # Cytoscape
        cyto.Cytoscape(
            id='org-chart', # pour le callback
            minZoom=0.2, # Zoom avant max
            maxZoom=2, # Zoom arrière max
            layout={'name': 'breadthfirst'}, # Style d'organigramme
            elements=my_elements, # voir partie configuration des composants
            style={'width': '100%', 'height': '500px'}, # Taille
            stylesheet=[
                
                # Group selectors pour le noeud (node) :
                # Affichage des titres pour chaque noeud
                {
                    'selector': 'node', # selector : soit node, soit edge
                    'style': {
                        'label': 'data(label)' # label : titre au noeud
                    }
                },

                # Group selectors pour le lien (edge) :
                # Affichage des textes insérés dans les liens
                {
                    'selector': 'edge', # selector : soit node, soit edge
                    'style': {
                        'label': 'data(weight)' # weight : titre au lien
                    }
                },

                # Class selectors : pour le noeud 'Executive Director (Harriet)' et
                # pour le lien entre 'Executive Director (Harriet)' et 
                # 'Vice President (Sarah)'
                # pour ce noeud et ce lien, on peut voir dans la partie 
                # configuration des composants que l'instruction
                # 'classes' : 'purple' a été insérée
                {
                    'selector': '.purple',
                    'style': {
                        'background-color': 'purple', # Couleur de fond
                        'line-color': 'purple' # Couleur du contour
                    }
                },
                
                # Class selectors pour les noeuds 'Vice President (Charlotte)'
                # et 'Vice President (Sarah)'
                {
                    'selector': '.square', # 'classes': 'square'
                    'style': {
                        'shape': 'square', # forme du noeud : carré
                    }
                },
                
                # Class selectors pour le noeud 'Program Associate (Ellen)'
                {
                    'selector': '.myimage', # 'classes': 'myimage'
                    'style': {
                        'width': 100, # Hauteur du noeud
                        'height': 100, # Taille du noeud
                        # Image insérée dans le noeud 
                        # (toujours dans le répertoire 'assets')
                        'background-image': ['./assets/sunny-and-cloud.jpg']
                    }
                },
                
                # Class selectors pour les noeuds 'Program Officer (Sojourner)' et
                # 'Program Officer (Elizabeth)'
                {
                    'selector': '.green', 
                    'style': {
                        'background-color': 'green', # Couleur de fond
                        'line-color': 'green' # Couleur du contour
                    }
                },
                
                # Class selectors pour les noeuds 'Program Officer (Sojourner)' et
                # 'Program Officer (Elizabeth)'
                {
                    'selector': '.diamond',
                    'style': {
                        'shape': 'diamond', # forme du noeud : diamant
                    }
                },

                # Condition : si la valeur attribuée au paramètre 'weight' pour
                # les liens (edge) est supérieure à 3, alors intervenir sur la 
                # taille de la largeur du lien
                # Pour chaque lien, un texte a été inséré qui est de type 'int'
                {
                    'selector': '[weight > 3]', 
                    'style': {
                        'width': 20
                    }
                },
                
                # Condition : si le titre attribué au noeud contient les lettres
                # 'rah', alors la couleur du noeud est noire
                {
                    'selector': '[label *= "rah"]',
                    'style': {
                        'background-color': '#000000',
                    }
                }
            ]
        )
    ], className='six columns'),

], className='row')

# INTERACTION DES COMPOSANTS ----------------------------------------------

# Mise à jour du style de l'organigramme selon la valeur choisie 
# dans le menu déroulant :
@callback(
    Output('org-chart', 'layout'), # Sortie : cytoscape
    Input('dpdn', 'value')) # Entrée : menu déroulant
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
        'name': layout_value,
        'roots': '[id = "ed"]',
        'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }


if __name__ == '__main__':
    app.run_server(debug=True, port=4000)
