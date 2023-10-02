"""
Lien : https://www.youtube.com/watch?v=hXAFzogkkKk&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=11
Cours : Markdown Component - Plotly Dash

Différents markdown avec raccourcis :
'data/Markdown_Ecriture.docx'

Documentation dcc.Markdown :
https://dash.plotly.com/dash-core-components/markdown

Date : 02-10-23
"""
from dash import Dash, dcc, html, callback, Input, Output

# FRONT END --------------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__, 
           external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Configuration de la page @
app.layout = html.Div([
    
    html.Div([
        
        # Titre H2
        html.H2("Text with Markdown"),
        
        # Zone de texte à saisir
        dcc.Textarea(
            id="message", # pour le callback
            placeholder="Test your Markdown", # Texte par défaut affiché
            style={'width': '100%', 'height': 300}), # Taille de la zone de texte
        
    ],className="four columns"),

    html.Div([
        
        # Barre de séparation vertichale
        html.Hr(
            style={"width":4, 
                   "height":700, 
                   "border": "6px solid black"})
        
    ],className="one columns"),

    html.Div([
        
        # Titre H2
        html.H2("Result"),
        
        # Markdown
        dcc.Markdown(id="markdown-result")
        
    ],className="seven columns"),

])

# INTERACTIONS DES COMPOSANTS -------------------------------------------------

# MAJ du markdown selon le texte saisie dansle composant Textarea
@callback(
    Output("markdown-result", "children"), # Sortie : Markdown
    Input("message", "value") # Entrée : Zone de texte à saisir
)
def text_update(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)
