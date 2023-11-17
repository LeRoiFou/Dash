"""
Lien : https://www.youtube.com/watch?v=Hc9_-ncr4nU&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=9
Cours : How to Make a Python Multi Page Application with Plotly Dash

Documentation sur les multi-pages :
https://dash.plotly.com/urls#dash-pages

Cours indexG007_MultiPage.py

Date : 17-11-2023
"""

from dash import dcc, html, register_page

# Instanciation de la librairie
register_page(__name__)

layout = html.Div(
    [   
        # Texte
        dcc.Markdown('# This will be the content of Page 3')
    ]
)