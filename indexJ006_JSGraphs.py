"""
Cours : Python Dash Apps with JavaScript Graphs - ApexCharts
Lien : https://www.youtube.com/watch?v=9x2VSjQUHUo

Librairie Dash Mantine composants :
https://www.dash-mantine-components.com/

Fichiers rattachés :
appexcahrts.js (répertoire assets)
herpers.js (répertoire assets)

Insertion d'un graphique JS dans Dash permettant d'avoir une meilleure 
présentation des données

Date : 15-02-24
"""

# Code belongs to yazid - https://github.com/leberber

from dash import  (Dash, dcc, html, Input, Output, clientside_callback,
                   ClientsideFunction)
import dash_mantine_components as dmc # librairie avec les composants qui tuent
from indexJ006_JSGraphs_data import tradeData # récup des données (liste de dict)

# Instanciation de la sous-librairie Dash et thème appliqué pour le graph JS
app = Dash(external_scripts=['https://cdn.jsdelivr.net/npm/apexcharts'])

# Configuration de la page @
app.layout = html.Div(
    children=[
        
        # Composant Store : récupération des données
        dcc.Store(id='ApexchartsSampleData', # pour le callback
                  data=tradeData, # données récupérées du fichier python
                  ),
        
        # Titre principal de la page @
        html.H1("Javascript Charts inside a Dash App",),
        
        # Contenu centré horizontalement et verticalement
        dmc.Center(
            
            # Arrière-plan de couleur blanc
            # https://www.dash-mantine-components.com/components/paper
            dmc.Paper(
                shadow="sm", # type d'ombre prédéfinie
                style={'height':'600px', # hauteur
                       'width':'800px', # largeur
                       'marginTop':'100px' # marge haut
                       },
                children=[ # contenu de l'arrière-plan
                    
                    # Zone vide pour le graphique
                    html.Div(id='apexAreaChart', # pour le callback
                             ),
                    
                    # Contenu centré horizontalement et verticalement
                    dmc.Center(
                        children=[
                            
                            # Boutons d'option
                            dmc.SegmentedControl(
                                id="selectCountryChip", # pour le callback
                                value="Canada", # Valeur affichée par défaut
                                data=[ # Valeurs conservées
                                    'Canada', 'USA', 'Australia',],
                            )
                        ]
                    )
                ]
            )
        )
    ]
)

# MAJ du graphique selon le pays sélectionné dans les boutons d'options avec les 
# données récupérées du fichier indexJ006_JSGraphs_data.py
clientside_callback(
    ClientsideFunction( # Données du fichier appexcarhts.js
        namespace='apexCharts', # nom de l'espace de données du fichier appexcarhts.js
        function_name='areaChart' # nom de la fonction du fichier appexcarhts.js
    ),
    Output("apexAreaChart", "children"), # Sortie : graphique
    Input("ApexchartsSampleData", "data"), # Entrée : données (store())
    Input("selectCountryChip", "value"), # Entrée : boutons d'option
)


if __name__ == "__main__":
    app.run_server(debug=True)
    