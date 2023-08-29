"""
Lien : https://www.youtube.com/watch?v=lKXePw01R2A
Cours : Create your Plotly Dash Multipage App - Beta Version

Dans ce cours, on dispose d'une liste des onglets dans une barre de menu située
en haut de la page @

Documentation : http://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/

Date : 29-08-23
"""

from dash import Dash, html, page_registry, page_container
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

# Instanciation de la librairie Dash
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    use_pages=True # récupération des fichiers .py dans le répertoire 'pages'
)

# Affichage des attributs des widgets de chaque fichier .py du répertoire page
# sous la forme de dictionnaires
# for x in page_registry.values():
#     print(x)

navbar = dbc.NavbarSimple(
    
    # Menu déroulant pour lister les onglets
    dbc.DropdownMenu(
        
        [   # Récupération des données de chaque fichier .py dans le répertoire
            # 'pages' : attributs des widgets en dictionnaire
            dbc.DropdownMenuItem(
                page["name"], # Nom du fichier à afficher dans le menu onglet
                href=page["path"]) # Extension de l'URL
            for page in page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True, # Mettre toujours True (mise en forme bouton liste onglets)
        label="Liste des onglets", # Menu déroulant dans la barre haut de la page @
    ),
    brand="Démonstration du recours à plusieurs onglets", # Titre barre haut page @
    color="primary", # Couleur de la barre haut
    dark=True, # Couleur de texte de la barre haut : True = couleur blanche !
    className="mb-2",
)

# Configuration de la page @
app.layout = dbc.Container(html.Div([
    navbar, 
    page_container
]), fluid=True) # Affichage sur la page entière

if __name__ == "__main__":
    app.run_server(debug=True)
