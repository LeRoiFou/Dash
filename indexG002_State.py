"""
Lien : https://www.youtube.com/watch?v=mTsZL-VmRVE&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=3
Cours : The Dash Callback - Input, Output, State, and more

Documentation sur les callback :
https://dash.plotly.com/basic-callbacks

prevent_initial_callback=True : réinitialisation des composants attendus en
sortie (output) appelés en callback -> pas de MAJ des composants attendus en 
sortie dès chargement de la page @

exceptions.PreventUpdate : permet d'éviter que la sortie de TOUS les composants 
soit MAJ dès que l'utilisateur déclenche le callback

no_update : permet d'éviter que la sortie de CERTAINS composants soit MAJ 
dès que l'utilisateur déclenche le callback

La fonction state à la différence de input dans le callback, ne modifie pas
la sortie du composant concernée du callback (output) -> ce n'est qu'en
intervenant sur l'"input" du composant concerné que le "state" devient par la 
suite un "input"

ATTENTION : un fonctionnalité (component_property) de sortie d'un composant ne
s'applique que pour un seul callback !!!

Date : 13-11-2023
"""

import pandas as pd
import plotly.express as px
from dash import (Dash, html, dcc, callback, Output, Input, State, 
                  exceptions, no_update)

# BACK END -----------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Mutual-Funds.csv")

# Assignation d'une liste de couleurs
colors = ["black", "blue", "red", "yellow", "pink", "orange"]

# FRONT END ---------------------------------------------------------------

# Instanciation de la librairie Dash
app = Dash()

# Configuration de la page @
app.layout = html.Div(
    children=[
        
        # Menu déroulant
        dcc.Dropdown(
            id='my-dropdown', # pour le callback
            multi=True, # affichage multiple valeurs
            options=[{'label': x, 'value': x} # valeurs du composant
                     for x in sorted(df.fund_extended_name.unique())],
            value=["Fidelity 500 Index Fund", # valeurs affichées par défaut
                   "Fidelity Advisor Freedom 2035 Fund Class A",
                   "Fidelity Freedom 2035 Fund",
                   ], 
            ),
        
        # Bouton d'exécution
        html.Button(
            id='my-button', # pour le callback
            n_clicks=0, # bouton non appuyé automatiquement lors du chargement page @
            children="Show breakdown", # texte affiché
            ),
        
        # Graphique (vide)
        dcc.Graph(
            id='graph-output', # pour le callback
            figure={}, # données vides
            ),

        # Zone pour texte à afficher
        html.Div(
            id="sentence-output", # pour le callback
            children=["This is the color I love"], # texte affiché
            style={}, # absence de style
            ),
        
        # Boutons d'option
        dcc.RadioItems(
            id='my-radioitem', # pour le callback
            value="black", # valeur cochée par défaut
            options=[{'label': c, 'value': c} for c in colors], # valeurs du composant
            ),
    ]
)

# INTERACTION DES COMPOSANTS -----------------------------------------------

# MAJ du diagramme circulaire (camembert) selon les données affichées au menu
# déroulant
@callback(
    Output(component_id='graph-output', # Sortie : graphique
           component_property='figure'),
    [Input(component_id='my-dropdown', # Entrée : menu déroulant
           component_property='value')],
    # [Input(component_id='my-button', # Entrée : bouton d'exécution
    #        component_property='n_clicks')],
    # [State(component_id='my-dropdown', # State : menu déroulant
    #        component_property='value')],
    prevent_initial_call=False # pas de réinit affichage sortie des composants
)
def update_my_graph(val_chosen):
    
    # S'il y a au moins une valeur affichée au menu déroulant...
    if len(val_chosen) > 0:
        # print(n)
        
        # Affichage de la valeur choisie au menu déroulant
        print(f"value user chose: {val_chosen}")
        
        # Type d'objet de la valeur choisie au menu déroulant
        print(type(val_chosen))
        
        # Recoupement dans la DF de la valeur choisie au menu déroulant
        dff = df[df["fund_extended_name"].isin(val_chosen)]
        
        # Configuration du graphique : diagramme circulaire (camembert)
        fig = px.pie(
            dff, # DF recoupée ci-avant
            values="ytd_return", # Valeurs à afficher
            names="fund_extended_name", # Valeurs pour la légende
            title="Year-to-Date Returns", # Titre du graphique
            )
        fig.update_traces(textinfo="value+percent", # Données à afficher
                          ).update_layout(title_x=0.5) # Alignement du titre
        
        # MAJ du graphique
        return fig
    
    # Si aucune valeur n'est affichée du menu déroulant
    elif len(val_chosen) == 0:
        
        # Exception : pas de MAJ du graphique
        raise exceptions.PreventUpdate


# # MAJ du diagramme circulaire selon la valeur choisie au menu déroulant et MAJ
# # de la zone de texte (couleur) selon la valeur choisie aux boutons d'options
# @callback(
#     [Output('graph-output', 'figure'), # Sortie : graphique
#      Output('sentence-output', 'style')], # Sortie : zone pour texte à afficher
#     [Input(
#         component_id='my-radioitem', # Entrée : boutons d'option
#         component_property='value'),
#      Input(
#          component_id='my-dropdown', # Entrée : menu déroulant
#          component_property='value')],
#     prevent_initial_call=False # pas de réinit affichage sortie des composants 
# )
# def update_graph(color_chosen, val_chosen):
    
#     # Si aucune valeur du menu déroulant n'a été choisie...
#     if len(val_chosen) == 0:
        
#         # Graphique non MAJ et affichage du texte selon la couleur choisie aux
#         # boutons d'option
#         return no_update, {"color": color_chosen}
    
#     # Si au moins une valeur du menu déroulant a été choisie...
#     else:
        
#         # Recoupement de la DF selon la valeur choisie au menu déroulant
#         dff = df[df["fund_extended_name"].isin(val_chosen)]
        
#         # Configuration du diagramme circulaire (camembert)
#         fig = px.pie(
#             dff, # DF recoupée ci-avant
#             values="ytd_return", # Valeurs à afficher
#             names="fund_extended_name", # Valeurs pour la légende
#             title="Year-to-Date Returns", # Titre du graphique
#             )
#         fig.update_traces(textinfo="value+percent" # Valeurs à afficher
#                           ).update_layout(title_x=0.5) # Alignement du titre
        
#         # MAJ du graphique + couleur du texte de la zone de texte selon la valeur
#         # choisie aux boutons d'option
#         return fig, {"color": color_chosen}


if __name__ == '__main__':
    app.run_server(debug=True)

    