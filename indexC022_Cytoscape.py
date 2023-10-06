"""
Lien : https://www.youtube.com/watch?v=Ip2x7mmrBYY&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=16
Cours : Dash Cytoscape - Layout and User Interaction

Documentation sur Cytoscape Reference :
https://dash.plotly.com/cytoscape/reference

Documentation sur Cytoscape Layouts :
https://dash.plotly.com/cytoscape/layout

Documentation sur Cytoscape Event Callbacks :
https://dash.plotly.com/cytoscape/events

Date : 06-10-23
"""

from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_cytoscape as cyto 
import pandas as pd 
import plotly.express as px
import math

# Load extra layouts
# cyto.load_extra_layouts()

# Importation du fichier .csv converti en DF pandas
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Cytoscape/org-data.csv")

# FRONT END -------------------------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la sous-librairie Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div([
    
    html.Div([
        
        # Menu déroulant
        dcc.Dropdown(
            id='dpdn', # pour le callback
            value='breadthfirst', # valeur par défaut affiché
            clearable=False, # valeur affiché non supprimable
            options=[ # valeurs du menu déroulant
                {'label': name.capitalize(), 'value': name}
                for name in ['breadthfirst' ,'grid', 'random', 
                             'circle', 'cose', 'concentric']
            ]
        ),
        
        # Cytoscape alimenté de la DF ci-avant
        cyto.Cytoscape(
            id='org-chart', # pour le callback
            autoungrabify=False, # True : noeuds figés
            minZoom=0.2, # zoom avant max
            maxZoom=1, # zoom arrière max
            layout={'name': 'breadthfirst'}, # Style d'organigramme
            
            # layout : selon le type d'organigramme sélectionné :
            
            # layout={
            #     'name': 'circle',
            #     'radius': 250,
            #     'startAngle': math.pi * 1 / 9,
            #     'sweep': math.pi * 1 / 3
            # },

            # layout={
            #     'name': 'grid',
            #     'rows': 2,
            #     'cols': 4
            # },

            # layout={
            #     'name': 'breadthfirst', # tree
            #     'roots': '[id = "Executive Director (Harriet)"]'
            #     # 'roots': '#vp1, #vp2'
            #
            # },

            style={'width': '100%', 'height': '500px'}, # Taille
            elements=
                [
                    # Noeuds
                    {'data': {'id': x, 'label': x}} for x in df.name
                ]
                +
                [
                    # Liens
                    {'data': {
                        'source': 'Executive Director (Harriet)', 
                        'target': 'Vice President (Sarah)'}},
                    {'data': {
                        'source': 'Executive Director (Harriet)', 
                        'target': 'Vice President (Charlotte)'}},
                    {'data': {
                        'source': 'Vice President (Sarah)', 
                        'target': 'Program Officer (Sojourner)'}},
                    {'data': {
                        'source': 'Vice President (Sarah)', 
                        'target': 'Program Officer (Elizabeth)'}},
                    {'data': {
                        'source': 'Vice President (Charlotte)', 
                        'target': 'Program Associate (Ellen)'}},
                ]
        )
        
    ], className='six columns'),

    html.Div([
        
        # Zone vide
        html.Div(id='empty-div', children='')
        
    ],className='one column'),

    html.Div([
        
        # Diagramme en barre alimenté de la DF récupérée ci-avant
        dcc.Graph(id='my-graph', 
                  figure=px.bar(df, x='name', y='slaves_freed'))
        
    ], className='five columns'),

], className='row')

# INTERACTION DES COMPOSANTS ------------------------------------------------

# Mise à jour du style de l'organigramme selon la valeur choisie 
# dans le menu déroulant :
@callback(
    Output('org-chart', 'layout'), # Sortie : cytoscape
    Input('dpdn', 'value')) # entrée : menu déroulant
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
        'name': layout_value,
        'roots': '[id = "Executive Director (Harriet)"]',
        'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }

# Titre affiché dans la zone vide à partir de la sélection sur le cytoscape et 
# affichage du résultat dans le terminal
@app.callback(
    Output('empty-div', 'children'), # Sortie : zone vide
    Input('org-chart', 'mouseoverNodeData'), # Entrée : cytoscape
    Input('org-chart','mouseoverEdgeData'), # Entrée : cytoscape
    Input('org-chart','tapEdgeData'), # Entrée : cytoscape
    Input('org-chart','tapNodeData'), # Entrée : cytoscape
    Input('org-chart','selectedNodeData') # Entrée : cytoscape
)
def update_layout(mouse_on_node, mouse_on_edge, tap_edge, tap_node, snd):
    print(f"Souris survolé sur le noeud : {mouse_on_node}")
    print(f"Souris survolé sur le lien : {mouse_on_edge}")
    print(f"Souris sélectionné sur le lien : {tap_edge}")
    print(f"Souris sélectionné sur le noeud : {tap_node}")
    print("------------------------------------------------------------")
    print(f"Tous les noeuds sélectionnés : {snd}")
    print("------------------------------------------------------------")

    return 'Voir le terminal pour les noeuds/liens survolés/sélectionnés.'

# Barre de diagramme de couleur jaune selon le noeud sélectionné dans le cytoscape
@app.callback(
    Output('my-graph','figure'), # Sortie : diagramme en barre
    Input('org-chart','tapNodeData'), # Entrée : cytoscape
)
def update_nodes(data):
    if data is None:
        return no_update # évite un message d'erreur
    else:
        # Copie de la DF
        dff = df.copy() 
        
        # Filtre de la DF selon la noeud sélectionné dans le cytoscape
        dff.loc[dff.name == data['label'], 'color'] = "yellow" 
        
        # MAJ du graphique
        fig = px.bar(dff, x='name', y='slaves_freed')
        fig.update_traces(marker={'color': dff['color']})
        
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
