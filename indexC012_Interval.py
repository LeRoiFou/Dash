"""
Lien : https://www.youtube.com/watch?v=OSFoBbNnPWk&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=6
Cours : The Dash Interval overview

Dans ce cours on utilise le composant dcc.Interval qui permet de mettre à jour les 
données qu'on pourrait éventuellement récupérer dans différents sites @ à partir
des API.

On a recours également à la sous-librairie dash.exceptions qui lève une exception
lors de la MAJ des données

Documentation composant dcc.Interval :
https://dash.plotly.com/dash-core-components/interval

Date : 25-09-2023
"""

from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

# Instanciation de la librairie
app = Dash(__name__)

# FRONT END----------------------------------------------------------------------

# Configuration de la page @
app.layout = html.Div([
    
    # Compteur
    dcc.Interval(
                id='my_interval',
                disabled=False, # Si True le compteur n'est plus mis à jour
                interval=1*3_000, # Incrémentation du nombre de compteur par milliseconds
                n_intervals=0, # Nombre affiché au compteur par défaut
                max_intervals=4, # Nombre affiché max au compteur
                # Si max_intervals=-1 (nombre par défaut) : aucune limite
                # Si max_intervals=0 : le compteur s'arrête
    ),

    # Zone vide pour le chiffre du compteur à afficher
    html.Div(id='output_data', style={'font-size':36}),
    
    # Zone de texte
    dcc.Input(id="input_text",type='text'),
    
    # Graphique vide
    dcc.Graph(id="mybarchart"),

])

# FRONT END & BACK END -------------------------------------------------------------

# MAJ du chiffre du compteur à afficher et du diagramme en barre
@app.callback(
    [Output('output_data', 'children'), # Sortie : chiffre à afficher
     Output('mybarchart', 'figure')], # Sortie : graphique
    [Input('my_interval', 'n_intervals')] # Entrée : compteur
)
def update_graph(num):
    """update every 3 seconds"""
    
    # Si le compteur est à 0
    if num==0:
        
        # Suppression de l'erreur affiché
        raise PreventUpdate
    else:
        
        # affiché du numéro du compteur
        y_data=num 
        
        # MAJ du diagramme en barre
        fig=go.Figure(data=[go.Bar(x=[1, 2, 3, 4, 5, 6, 7, 8, 9], 
                                   y=[y_data]*9)],
                      layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
        )

    return (y_data,fig)

# MAJ du compteur selon si le mot 'stop' est affiché dans la zone de texte
@app.callback(
    Output('my_interval', 'max_intervals'), # Sortie : compteur
    [Input('input_text', 'value')] # Entrée : zone de texte
)
def stop_interval(retrieved_text):
    
    # Si 'stop' est affiché dans la zone de texte
    if retrieved_text == 'stop':
        
        # Arrêt du compteur
        max_intervals = 0
    
    else:
        
        # Suppression de l'erreur affiché
        raise PreventUpdate

    return (max_intervals)
#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
