"""
Lien : https://www.youtube.com/watch?v=wmQ6_GZ0zSk
Cours : Build Python Data Apps with Vizro Dash

Démonstration de la librairie Vizro :
https://vizro.mckinsey.com/country-analysis

Documentation sur Vizro :
https://vizro.readthedocs.io/en/stable/pages/tutorials/first_dashboard/

Exemple avec des graphiques

Date : 04-12-2023
"""

import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm

# Récupération des données
df = px.data.iris()
print(df.head())

# Configuration des composants
page = vm.Page(
    
    # Titre principal
    title="My first dashboard",
    
    # Composants de la page @
    components=[
        
        # Nuage de points
        vm.Graph(id="scatter_chart", 
                 figure=px.scatter(
                     df, 
                     x="sepal_length",
                     y="petal_width", 
                     color="species")),
        
        # Diagramme en barre
        vm.Graph(id="hist_chart", 
                 figure=px.histogram(
                     df, 
                     x="sepal_width", 
                     color="species")),
    ],
    
    # Assimilée à un callback : les données du diagramme en barre s'adaptent
    # par rapport à la donnée sélectionnée dans le menu déroulant
    controls=[
        # Menu déroulant effectuant un filtre pour le diagramme en barres
        vm.Filter(column="sepal_width", # champ de la DF ciblée
                  selector=vm.Dropdown(), # filtre par le menu déroulant
                  targets=["hist_chart"]), # cible : diagramme en barre
    ],
)

# Configuration de la page @
dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
