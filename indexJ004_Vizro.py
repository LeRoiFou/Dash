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

# Récupération des données converties en DF
df = px.data.iris()
dff = px.data.gapminder()

# Configuration des composants
page = vm.Page(
    
    # Titre principal de la page @
    title="My first dashboard",
    
    # Composants
    components=[
        
        # Nuage de points
        vm.Graph(id="scatter_chart", 
                 figure=px.scatter(df, 
                                   x="sepal_length",
                                   y="petal_width", 
                                   color="species")),
        
        # Diagramme en barre
        vm.Graph(id="hist_chart", 
                 figure=px.histogram(
                     dff, x="continent", 
                     y="gdpPercap", 
                     range_y=[0,5_000_000])),
    ],
    
    # Assimilé à un callback
    controls=[
        # use the dropown to update (target) the x attribute of the scatter chart
        # scatter chart attributes: 
        # https://plotly.com/python-api-reference/generated/plotly.express.scatter.html#plotly.express.scatter
        vm.Parameter(selector=vm.Dropdown(options=["sepal_length","petal_length"],
                                          multi=False,
                                          value="sepal_length",
                                          title="X axis"),
                     targets=["scatter_chart.x"]),
        
        # use the rangeSlider to update (target) 
        # the range_y attribute of the histogram
        # histogram attributes: 
        # https://plotly.com/python-api-reference/generated/plotly.express.histogram.html#plotly.express.histogram
        vm.Parameter(selector=vm.RangeSlider(min=0,
                                             max=9_000_000,
                                             value=[0,5_000_000],
                                             step=1_000_000,
                                             title="Y axis Range"),
                     targets=["hist_chart.range_y"])
    ],
)

# Configuration de la page @
dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
