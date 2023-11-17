"""
Lien : https://www.youtube.com/watch?v=Hc9_-ncr4nU&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=9
Cours : How to Make a Python Multi Page Application with Plotly Dash

Documentation sur les multi-pages :
https://dash.plotly.com/urls#dash-pages

Multi-page : présentation sommmaire

Date : 17-11-2023
"""

from dash import Dash, html, dcc, page_registry, page_container

# Instanciation de la librairie Dash + info multi-pages
app = Dash(use_pages=True)

# Configuration de la page @
app.layout = html.Div(
    [
        # Titre de la page @
        html.Div("Python Multipage App with Dash", 
                 style={'fontSize':50, 'textAlign':'center'},
                 ),
        
        
        html.Div([
            
            # Liens
            dcc.Link(
                page['name']+"  |  ", # Ligne avec les noms des onglets
                href=page['path']) # Référence d'accès
            for page in page_registry.values() # onglets
        ]),
        
        # Ligne séparatrice
        html.Hr(),

        # Contenu de chaque page
        page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
    