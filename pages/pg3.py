"""
Lien : https://dash.plotly.com/urls#dash-pages
Cours : https://dash.plotly.com/urls#dash-pages

Fichier principal : indexG008_MultiPage.py

Date : 18-11-2023
"""

from dash import register_page, dcc, html

# Configuration de l'onglet
register_page(__name__, name='Other Data')

# Configuration de la page @
layout = html.Div(
    [   
        # Texte
        dcc.Markdown('# This will be the content of Page 3 and much more!')
    ]
)