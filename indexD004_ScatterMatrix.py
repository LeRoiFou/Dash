"""
Lien : https://www.youtube.com/watch?v=NuoA08b-cMM&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=5
Cours : Scatter Matrix (Confirm Dialog) - Python Dash Plotly

Documentation sur plotly.express.scatter_matrix (matrice de dispersion):
https://plotly.com/python-api-reference/generated/plotly.express.scatter_matrix.html#plotly.express.scatter_matrix

Documentation sur dcc.ConfirmDialog (message d'information):
https://dash.plotly.com/dash-core-components/confirmdialog

Documentation sur Customizing Hover text with Plotly Express (survolement texte)
https://plotly.com/python/hover-text-and-formatting/#disabling-or-customizing-hover-of-columns-in-plotly-express

Cours sur le composant matrice de dispersion (px.scatter_matrix) et sur le
composant qui affiche un message d'information (dcc.ConfirmDialog).
Recours à la sous-librairie no_update qui permet de ne pas MAJ un composant
Documentation sur le texte affiché en survolant un composant (hover)

Date : 14-10-2023
"""

from dash import Dash, html, dcc, callback, Output, Input, no_update
import pandas as pd
import plotly.express as px

# DS -----------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv('assets/social_capital.csv')

# Suppression de champs
df.drop(['Alt FIPS Code','FIPS Code','State Abbreviation'], axis=1, inplace=True)

# FRONT END --------------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
    
    # Boîte de dialogue
    dcc.ConfirmDialog(
        id='confirm-dialog', # pour le callback
        displayed=False, # pas d'affichage par défaut
        message='Please choose Dropdown variables!', # affichage si exigé
    ),

    # Titre H1
    html.H1("Scatter Matrix of USA Social Capital Project", 
            style={'textAlign':'center'},
            ),

    # Menu déroulant
    dcc.Dropdown(
        id='my-dropdown', # pour le callback
        options=[{'label': s, 'value': s} for s in df.columns], # valeurs
        value=[ # affichage par défaut
            "% children 4+ hours on electronic device past week",
            "% children read to every day past week",
            "% children 4+ hours television past week",
            "% women currently married"],
        multi=True, # affichage multiple
    ),

    # Graphique
    dcc.Graph(
        id="my-chart", # pour le callback
        figure={}, # données vides
        ),
])


# INTERACTION DES COMPOSANTS ----------------------------------------------

# Si des valeurs ont été sélectionnés dans le menu déroulant : affichage
# des matrices de dispersion sinon, affichage d'un message d'information
@callback(
     Output( # Sortie : message d'information
         component_id='confirm-dialog', 
         component_property='displayed',), # résultat booléen (voir ci-après)
     Output( # Sortie : graphique
         component_id='my-chart', 
         component_property='figure',),
     Input( # Entrée : menu déroulant
         component_id='my-dropdown', 
         component_property='value',)
)
def update_graph(dpdn_val):
    
    # Si le nombre de valeurs affichés dans le menu déroulant est > à 0
    if len(dpdn_val) > 0:
        
        # MAJ du graphique : nuage de points multiple
        fig = px.scatter_matrix(
            df, # DF
            # dimensions : affichage des nuages de points selon les valeurs
            # sélectionnées dans le menu déroulant
            dimensions=dpdn_val,
            color='population', # couleur par rapport à la population
            hover_data={'State': True, # affichage complémentaire : État
                        'population': ':,' # population avec séparateur milliers
                        },
            )
        
        fig.update_traces(
            diagonal_visible=False, # Diagonale présente sur le graph (inutile)
            showupperhalf=True, # False : affichage en escalier des graphiques
            showlowerhalf=True, # False : affichage en escalier des graphiques
            )
        
        fig.update_layout(
            yaxis1={'title':{'font':{'size':3}}}, 
            yaxis2={'title':{'font':{'size':3}}},
            yaxis3={'title':{'font':{'size':3}}}, 
            yaxis4={'title':{'font':{'size':3}}},
            yaxis5={'title':{'font':{'size':3}}}, 
            yaxis6={'title':{'font':{'size':3}}},
            yaxis7={'title':{'font':{'size':3}}}, 
            yaxis8={'title':{'font':{'size':3}}},
            )
       
        fig.update_layout(
            xaxis1={'title':{'font':{'size':3}}}, 
            xaxis2={'title':{'font':{'size':3}}},
            xaxis3={'title':{'font':{'size':3}}}, 
            xaxis4={'title':{'font':{'size':3}}},
            xaxis5={'title':{'font':{'size':3}}}, 
            xaxis6={'title':{'font':{'size':3}}},
            xaxis7={'title':{'font':{'size':3}}}, 
            xaxis8={'title':{'font':{'size':3}}},
            )
        
        # False : Le message d'information ne s'affiche pas
        # fig : MAJ du graphique
        return False, fig

    # Si aucune valeur n'est affichée dans le menu déroulant
    if len(dpdn_val)==0:
        
        # True : Affichage du message d'information
        # no_update : graphique non MAJ
        return True, no_update


if __name__ == '__main__':
    app.run_server(debug=True)
