"""
Lien : https://www.youtube.com/watch?v=wmQ6_GZ0zSk
Cours : Build Python Data Apps with Vizro Dash

Démonstration de la librairie Vizro :
https://vizro.mckinsey.com/country-analysis

Documentation sur Vizro :
https://vizro.readthedocs.io/en/stable/pages/tutorials/first_dashboard/

Date : 04-12-2023
"""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.actions import filter_interaction

# Récupération des données converties en DF
df_gapminder = px.data.gapminder().query("year == 2007")

# Configuration de la page @
dashboard = vm.Dashboard(
    pages=[
        
        vm.Page(
            
            # Titre principal de la page @
            title="Filter interaction",
            
            # Composants
            components=[
                
                # Boîte à moustaches
                vm.Graph(
                    id="bar_relation_2007",
                    figure=px.box(
                        df_gapminder,
                        x="continent",
                        y="lifeExp",
                        color="continent",
                        points="all",
                        custom_data=["continent"], # 1 graphique par continent
                    ),
                    # clicking the custom_data (continent) of box plot will filter
                    # (target) the dataframe (continent column) 
                    # of gapminder_scatter graph
                    actions=[vm.Action(
                        function=filter_interaction(
                            targets=["gapminder_scatter"]))],
                ),
                
                # Nuage de points
                vm.Graph(
                    id="gapminder_scatter",
                    figure=px.scatter(
                        df_gapminder,
                        x="gdpPercap",
                        y="lifeExp",
                        size="pop",
                        color="continent",
                    ),
                ),
            ],
        ),
    ]
)

Vizro().build(dashboard).run()
