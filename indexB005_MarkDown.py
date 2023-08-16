"""
Dans ce script, on intervient sur le markdown pour saisir des blocs de texte

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Bloc de texte
markdown_text = '''
### Dash and Markdown
Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/) specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Markdown
    dcc.Markdown(children=markdown_text)
])

if __name__ == '__main__':
    app.run_server(debug=True)
    