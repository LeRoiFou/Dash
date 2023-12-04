"""
Lien : https://www.youtube.com/watch?v=wmQ6_GZ0zSk
Cours : Build Python Data Apps with Vizro Dash

Démonstration de la librairie Vizro :
https://vizro.mckinsey.com/country-analysis

Documentation sur Vizro :
https://vizro.readthedocs.io/en/stable/pages/tutorials/first_dashboard/

Multipage

Date : 04-12-2023
"""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro

# Récupération des données converties en DF
gapminder = px.data.gapminder().query("year == 2007")
df = px.data.iris()

# Configuration de la page
page1 = vm.Page(
    
    # Titre principal
    title="Page 1",
    
    # Composants
    components=[
        
        # Carte
        vm.Card(text="""This data app will explore the consequences of..."""),
        
        # Nuage de points
        vm.Graph(id="scatter_chart", 
                 figure=px.scatter(
                     df, 
                     x="sepal_length",
                     y="petal_width", 
                     color="species")),
        
        # Diagramme
        vm.Graph(id="hist_chart",
                 figure=px.histogram(
                     df, 
                     x="sepal_width", 
                     color="species")),
    ],
    
    # Assimilé au callback
    controls=[
        vm.Filter(column="species", selector=vm.Dropdown(value=["ALL"])),
    ],
)

# Configuration de la page
page2 = vm.Page(
    
    # Titre principal
    title="Page 2",
    
    path="world-order",
    
    # Composants
    components=[
        
        # Diagramme circulaire
        vm.Graph(
            id="sunburst", 
            figure=px.sunburst(gapminder, 
                               path=["continent", "country"], 
                               values="pop", 
                               color="lifeExp")
        )
    ],
    
    # Assimilé au callback
    controls=[
        vm.Filter(column="continent", targets=["sunburst"]),
        vm.Parameter(targets=["sunburst.color"], 
                     selector=vm.RadioItems(
                         options=["lifeExp", "pop"], 
                         title="Color")),
    ],
)

# Configuration de la page @
dashboard = vm.Dashboard(pages=[page1, page2])

Vizro().build(dashboard).run()
