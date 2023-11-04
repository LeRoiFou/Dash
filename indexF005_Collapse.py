"""
Lien : https://www.youtube.com/watch?v=RnJGlgc9vcM&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=7
Cours : Bootstrap Collapse Dash Plotly

Documentation sur collapse :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/

Dans ce programme, on apprend à masquer des composants avec le composant
dbc.collapse

Date : 04-11-2023
"""

from dash import Dash, html, callback, Input, Output, State      
import dash_bootstrap_components as dbc       

# FRONT END -------------------------------------------------------------

# Instanciation de la librairie et mise en page @
app = Dash(external_stylesheets=[dbc.themes.LUMEN])

# Configuration de la page @
app.layout = html.Div([
    
    html.Div(
        
        # Titre H6
        html.H6("Product: a beautiful Pizza reheated after a day in the fridge, for $99"), 
        style={"text-align":"center"},
        ),
    
    # Lige séparatrice
    html.Hr(),
    
    # Carte en-tête
    dbc.CardHeader(
        
            # Bouton d'exécution
            dbc.Button(
                "Why should I buy reheated pizza for $99?", # Texte affiché
                color="link", # Couleur du bouton
                id="button-question-1", # pour le callback
            )
    ),
    
    # Zone masquée
    dbc.Collapse(
        
        # Carte corps principal
        dbc.CardBody("Because it's a lot better than a hotdog."),
        id="collapse-question-1", # pour le callback
        is_open=False, # False : zone masquée
    ),

    # Carte en-tête
    dbc.CardHeader(
        
            # Bouton d'exécution
            dbc.Button(
                "Does it have extra cheese?", # Texte affiché
                color="link", # Couleur du bouton
                id="button-question-2", # pour le callback
            )
    ),
    
    # Zone masquée
    dbc.Collapse(
        
        # Carte corps principal
        dbc.CardBody("Yes, and it is made from the goats of Antarctica, which keeps the cheese cold and fresh."),
        id="collapse-question-2", # pour le callback
        is_open=False, # False : zone masquée
    ),
])

# INTERACTION DES COMPOSANTS --------------------------------------------------

# Après avoir appuyé sur le bouton d'exécution, affichage d'un texte masqué
# préalablement
@callback(
    Output("collapse-question-1", "is_open"), # Sortie : carte corps principal
    [Input("button-question-1", "n_clicks")], # Entrée : bouton d'exécution
    [State("collapse-question-1", "is_open")], # State : carte corps principal
)
def toggle_collapse(n, is_open):
    
    # Si le bouton est à nouveau appuyé 
    if n:
        # Données de la zone à nouveau masquées
        return not is_open
    
    # Affichage de la zone masquée
    return is_open

# Après avoir appuyé sur le bouton d'exécution, affichage d'un texte masqué
# préalablement
@app.callback(
    Output("collapse-question-2", "is_open"), # Sortie : carte corps principal
    [Input("button-question-2", "n_clicks")], # Entrée : bouton d'exécution
    [State("collapse-question-2", "is_open")], # State : carte corps principal
)
def toggle_collapse(n, is_open):
    
    # Si le bouton est à nouveau appuyé 
    if n:
        
        # Données de la zone à nouveau masquées
        return not is_open
    
    # Affichage de la zone masquée
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=2000)
