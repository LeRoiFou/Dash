"""
Lien : https://www.youtube.com/watch?v=g8xBlilTV4w&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=17
Cours : Introduction to Dash Cytoscape - Networks

Documentation sur Cytoscape Reference :
https://dash.plotly.com/cytoscape/reference

Complément de cours sur le cytoscape : une des barres du diagramme en barres change
de couleur selon le noeud sélectionné dans l'organigramme (cytoscape)

Concernant le layout de ce composant (configuration du composant sur la page @),
on utilise le paramètre 'preset' : layout={'name': 'preset'}, 
L'intérêt de ce paramètre, est qu'on peut personnaliser la position des noeuds
du cytoscape dans la page @

Date : 07-10-23
"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_cytoscape as cyto 
import pandas as pd 
import plotly.express as px

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/org-data.csv")

# FRONT END -----------------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la sous-librairie Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div([
    
    html.Div([
        
        # Cytoscape
        cyto.Cytoscape(
            id='org-chart', # pour le callback
            layout={'name': 'preset'}, # Style d'organigramme
            style={'width': '100%', 'height': '500px'}, # Taille
            elements=[ # Alimentation des données
                      
                # Noeuds
                
                {'data': {
                    'id': 'ed', 
                    'label': 'Executive Director (Harriet)'},
                 'position': {'x': 150, 'y': 50}, # position des noeuds (sympa ça)
                 'locked': True # True : noeud non déplacable
                },

                {'data': {
                    'id': 'vp1', 
                    'label': 'Vice President (Sarah)'},
                 'position': {'x': 0, 'y': 150}, # position des noeuds (sympa ça)
                 'grabbable': False # similaire à 'locked'
                },

                {'data': {
                    'id': 'vp2', 
                    'label': 'Vice President (Charlotte)'},
                 'position': {'x': 300, 'y': 150}, # position des noeuds (sympa ça)
                 'selectable': False # couleur du noeud non changé si sélection
                },

                {'data': {
                    'id': 'po1', 
                    'label': 'Program Officer (Sojourner)'},
                 'position': {'x': -100, 'y': 250}, # position des noeuds (sympa ça)
                 'selected': True # sélection par défaut
                },

                {'data': {
                    'id': 'po2', 
                    'label': 'Program Officer (Elizabeth)'},
                 'position': {'x': 150, 'y': 250} # position des noeuds (sympa ça)
                },

                {'data': {
                    'id': 'pa', 
                    'label': 'Program Associate (Ellen)'},
                 'position': {'x': 300, 'y': 350} # position des noeuds (sympa ça)
                },

                # Liens
                
                {'data': {'source': 'ed', 
                          'target': 'vp1'}},
                
                {'data': {'source': 'ed', 
                          'target': 'vp2'}},
                
                {'data': {'source': 'vp1', 
                          'target': 'po1'}},
                
                {'data': {'source': 'vp1', 
                          'target': 'po2'}},
                
                {'data': {'source': 'vp2', 
                          'target': 'pa'}},
            ]
        )
    ], className='six columns'),

    html.Div([
        
        # Graphique vide
        dcc.Graph(id='my-graph')
        
    ], className='six columns'),

], className='row')

# INTERACTION DES COMPOSANTS ---------------------------------------------

# Alimentation du graphique et couleur de la barre en fonction du noeud
# sélectionné dans l'organigramme (cytoscape)
# (tapNodeData : sélection du noeud avec la souris - voir indexC022)
@callback(
    Output('my-graph','figure'), # Sortie : graphique
    Input('org-chart','tapNodeData'), # Entrée : cytoscape - noeud sélectionné
)
def update_nodes(data):
    
    # Si aucun noeud n'est sélectionné dans l'organigramme (cytoscape)
    if data is None:
        
        # Copie de la DF
        dff = df.copy()
        
        # Filtre sur la DF
        dff.loc[dff.name == 'Program Officer (Sojourner)', 'color'] = "yellow"
        
        # Alimentation du diagramme en barres
        fig = px.bar(dff, x='name', y='slaves_freed')
        
        # Couleur des barres selon les données du champ 'color' de la DF
        fig.update_traces(marker={'color': dff['color']})
        
        return fig
    
    # Si un noeud est sélectionné
    else:
        
        print(data)
        
        # Copie de la DF
        dff = df.copy()
        
        # Filtre sur la DF
        dff.loc[dff.name == data['label'], 'color'] = "yellow"
        
        print(dff)
        
        # Alimentation du diagramme en barres
        fig = px.bar(dff, x='name', y='slaves_freed')
        
        # Couleur des barres selon les données du champ 'color' de la DF
        fig.update_traces(marker={'color': dff['color']})
        
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
