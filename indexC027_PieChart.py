"""
Cours : Pie Chart with the Dropdown in Python - Plotly Dash
Lien : https://www.youtube.com/watch?v=2pQQ9xg8wcQ

Lien sur les données traitées :
https://ourworldindata.org/grapher/domain-notable-artificial-intelligence-systems

Présentation de l'IA dans différentes domaines au fil des années

Date : 15-02-24
"""

from dash import Dash, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# BACK END --------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/domain-notable-ai-system.csv")

# Filtre appliqué sur la DF : domaine d'intervention
df = df[df.Entity != "Not specified"]

# FRONT END -------------------------------------------------------------

# Instanciation de la librairie Dash et thème appliqué
app = Dash(external_stylesheets=[dbc.themes.SPACELAB])

# Configuration de la page @
app.layout = dbc.Container(
    [
        # Texte markdown : H2 (titre principal) et H5 (commentaires)
        dcc.Markdown("## Domain of notable artificial intelligence systems, \
                     by year of publication\n"
                     "###### Specific field, area, or category in which an \
                     AI system is designed to operate or solve problems."),
        
        # Ligne suivante       
        dbc.Row(
            [   
                
                # 1ère colonne de largeur 6
                dbc.Col(
                    
                    # Carte
                    dbc.Card(
                        
                        # Contenu de la carte
                        dbc.CardBody([
                            
                            # Graphique circulaire (zone vide)
                            dcc.Graph(id='domain-graph', # pour le callback
                                      ), 
                            
                            # Menu déroulant sur les années
                            dcc.Dropdown(
                                id="year-slct", # pour le callback
                                options=df['Year'].unique(), # contenu
                                value='2020', # valeur affichée
                                ) 
                        ]),
                        className="my-3" # fichier .css
                    ),
                    width=6
                ),
                
                # 2ème colonne de largeur 6
                dbc.Col(
                    
                    # Carte
                    dbc.Card(
                        
                        # Contenu de la carte
                        dbc.CardBody([
                            
                            # Graphique linéaire (zone vide)
                            dcc.Graph(id='line-graph', # pour le callback
                                      ),
                            
                            # Menu déroulant sur les domaines d'intervention
                            dcc.Dropdown(
                                id="domain-slct", # pour le callback
                                multi=True, # affichage multiple
                                options=sorted(df['Entity'].unique()), # contenu
                                value=['Multimodal', 'Language'], # valeurs affichées
                                )
                        ]),
                        className="my-3"
                    ),
                    width=6
                ),
            ]
        )
    ]
)

# INTERACTION DES COMPOSANTS ----------------------------------------------------

# MAJ du graphique circulaire selon l'année sélectionnée au menu déroulant
@callback(
    Output("domain-graph", "figure"), # Sortie : graphique circulaire
    Input("year-slct", "value"), # Entrée : menu déroulant sur les années
)
def update_pie_chart(year_chosen):
    
    # Récupération de l'année sélectionnée du menu déroulant convertie en type int
    year_chosen = int(year_chosen)
    
    # Filtre de la DF selon l'année sélectionnée
    df_dom_filtrd = df[df['Year'] == year_chosen]
    
    # Configuration du graphique circulaire
    pie_chart = px.pie(
        df_dom_filtrd, # DF traitée ci-avant
        names='Entity', # Champ ciblé
        values='Annual number of AI systems by domain', # Valeurs à insérer (en %)
        )
    
    # MAJ du graphique circulaire
    return pie_chart

# MAJ du graphique linéaire selon le ou les domaine(s) d'intervention en IA
@callback(
    Output("line-graph", "figure"), # Sortie : graphique linéaire
    Input("domain-slct", "value"), # Entrée : menu déroulant sur les domaines
)
def update_line_graph(domains_chosen):
    
    # 1er traitement de la DF : année > à 1999 (IA avant...)
    df_filtrd = df[df['Year']>1999]
    
    # 2ème traitement : recoupement de la DF selon la valeur sélectionnée au menu
    # déroulant sur le ou les domaine(s) d'intervention
    df_filtrd = df_filtrd[df_filtrd['Entity'].isin(domains_chosen)]
    
    # Configuration du graphique
    line_graph = px.line(
        df_filtrd, # DF traitée ci-avant
        x='Year', # Valeurs pour l'axe des abscisses
        y='Annual number of AI systems by domain', # Valeurs pour l'axe des ordonnées
        color='Entity', # Couleur de la ligne à partir du champ 'Entity' de la DF
        )
    
    # MAJ du graphique linéaire
    return line_graph


if __name__ == "__main__":
    app.run(debug=True)