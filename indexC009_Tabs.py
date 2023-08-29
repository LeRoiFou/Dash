"""
Lien : https://www.youtube.com/watch?v=lKXePw01R2A
Cours : Create your Plotly Dash Multipage App - Beta Version

Dans ce cours, cette fois-ci le menu se trouve à gauche de la fenêtre, après
avoir appuyé sur un bouton

Documentation : http://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/

Date : 29-08-23
"""

from dash import Dash, dcc, html, Output, Input, State, page_registry, page_container
import dash_labs as dl # pip install dash_labs
import dash_bootstrap_components as dbc

# Instanciation de la librairie Dash
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    use_pages=True # récupération des fichiers .py dans le répertoire 'pages
)

offcanvas = html.Div(
    [   
        # Bouton pour afficher la liste des onglets
        dbc.Button("Liste des onglets",  # Titre du bouton
                   id="open-offcanvas", # pour le callback
                   n_clicks=0), # ???
        
        # Menu de la liste des onglets
        dbc.Offcanvas(
            
            # Liste des onglets
            dbc.ListGroup(
                [   # Récup des données de chaque fichier .py dans le répertoire
                    # 'pages' : attributs des widgets en dictionnaire
                    dbc.ListGroupItem(
                        page["name"], # om du fichier à afficher dans le menu onglet
                        href=page["path"]) # Extension de l'URL
                    for page in page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ]
            ),
            id="offcanvas", # pour le callback
            is_open=False, # True : affichage de la liste dès ouverture page @
        ),
    ],
    className="my-3"
)

# Configuration de la page @
app.layout = dbc.Container(html.Div([
    offcanvas, 
    page_container
]), fluid=True) # Affichage sur la page entière

#---------------------------------------------------------------------------

@app.callback(
    Output( # Sortie : menu de la liste des onglets
        "offcanvas", 
        "is_open"), # Fonctionnalité : affichage du menu
    Input( # Entrée : bouton pour afficer la liste des onglets
        "open-offcanvas", 
        "n_clicks"), # Fonctionnalité : ???
    [State(
        "offcanvas", 
        "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
    