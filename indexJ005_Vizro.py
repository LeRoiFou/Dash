"""
Lien : https://www.youtube.com/watch?v=wmQ6_GZ0zSk
Cours : Build Python Data Apps with Vizro Dash

Démonstration de la librairie Vizro :
https://vizro.mckinsey.com/country-analysis

Documentation sur Vizro :
https://vizro.readthedocs.io/en/stable/pages/tutorials/first_dashboard/

Exemple ici avec une table

Date : 04-12-2023
"""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.tables import dash_data_table

# Récupération des données converties en DF
df = px.data.gapminder().query("year == 2007")

# Configuration des composants
page = vm.Page(
    
    # Titre principal de la page @
    title="Example of a Dash DataTable",
    
    # Composants : table
    components=[
        vm.Table(id="table", 
                 title="Dash DataTable", 
                 figure=dash_data_table(data_frame=df, editable=True)),
    ],
    
    # Assimilé au callback
    controls=[
        vm.Parameter(selector=vm.Dropdown(
            options=[{"label":"True", "value":True},
                     {"label":"False", "value":False}],
            multi=False,
            value=True,
            title="Editable Cells"),
                     targets=["table.editable"]),
              ],
)

# Configuration de la page @
dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
