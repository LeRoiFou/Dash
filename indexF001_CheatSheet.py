"""
Lien : https://www.youtube.com/watch?v=VTO6Njy10dY&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=2
Cours : How to Style your Dash App with Bootstrap Cheat Sheet

Documentation sur Cheat Sheet : 
https://dashcheatsheet.pythonanywhere.com/

Mise en forme de la page @ en recourant pour exemple du lien ci-avant

Date : 25-10-2023
"""

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

# DS ----------------------------------------------------------------------

# Récupération des données de la DF de la librairie plotly express
df = px.data.tips()

# Récupération uniquement des valeurs uniques : jour
days = df.day.unique()

# CONFIGURATION DES COMPOSANTS ---------------------------------------------

# Configuration du menu déroulant n° 1
day_dropdown = dcc.Dropdown(
    id="dropdown", # pour le callback
    options=[{"label": x, "value": x} 
             for x in days], # valeurs composant
    value=days[0], # valeur affichée par défaut
    clearable=False, # valeur affichée non supprimable
    className="mt-3",
)

# Configuration du menu déroulant n° 2
fake_dropdown = dbc.Select(
    id="fake-bootstrap-dropdown", # pour le callback (non utilisé ici)
    options=[{"label": x, "value": x} 
             for x in df.sex.unique()], # valeurs composant
    value="", # valeur affichée par défaut
    placeholder="Fake disconnected dropdown for tutorial purposes", 
    # Titre par défaut affiché dans le menu déroulant
    className="bg-success mt-3"
)

# FRONT END ---------------------------------------------------------------

# Instanciation de la librairie Dash
app = Dash(external_stylesheets=[dbc.themes.COSMO],
           )

# Configuration de la page @
app.layout = dbc.Container([
    
    # Saut de ligne
    html.Br(),
    
    # Configuration des bordures
    html.Span("Utility Border", 
              className="border",
              # border-top, border border-danger, border border-3, 
              # border rounded-circle
              ),  
    
    # Configuration des couleurs
    html.Div("Utility Color", 
             className="text-primary", # text-light, bg-success
             ),  
    
    # Configuration de l'opacité 
    html.Div("Utility Opacity",  
             className="opacity-25", # opacity-75
             ), 
    
    # Configuration de l'espacement
    html.Div("Utility Spacing", 
             className="border m-2", # m-5, ms-2, my-4, p-3, pb-5
             ),  
    
    # Configuration du débordement du texte 
    html.Div("Utility Text : with nowrap", 
             style={"width":15}, 
             className="text-nowrap",
            # text-wrap, text-break, fs-3, text-decoration-line-through
             ),  
    
    # Configuration du texte en markdown
    html.Div(["Utility Typography : you can use html.Mark to ", 
              html.Mark("highlight"), 
              " text",
              ]),
    
    # Combinaison des configurations ci-avant
    html.Div("Example of many classes combined",
             className="opacity-100 p-2 m-1 bg-primary text-light fw-bold rounded",
             ),

    dbc.Row([
        dbc.Col(
            
            # Menu déroulant n° 1
            day_dropdown, 
            width=6),
        
        dbc.Col(
            
            # Menu déroulant n° 2
            fake_dropdown, 
            width=6)
    ]),
    dbc.Row([
        dbc.Col(
            
            # Graphique (vide)
            dcc.Graph(id="bar-chart", # pour le callback
                      ), width=12)
    ]),
])

# INTERACTION DES COMPOSANTS -------------------------------------------

# MAJ du diagramme en barres selon la valeur sélectionnée dans le menu 
# déroulant n° 1
@callback(
    Output("bar-chart", "figure"), # Sortie : graphique
    [Input("dropdown", "value")]) # Entrée : menu déroulant n° 1
def update_bar_chart(day):
    
    # Filtre sur la DF selon la valeur du menu déroulant n° 1
    mask = df["day"] == day
    
    # MAJ du graphique : diagramme en barres
    fig = px.bar(df[mask], # DF filtrée
                 x="sex", # Axe des abscisses
                 y="total_bill", # Axe des ordonnées
                 color="smoker", # couleur des barres selon ce champ
                 barmode="group", # groupement des barres
                 )
    
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8002)
