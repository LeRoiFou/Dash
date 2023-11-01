"""
Lien : https://www.youtube.com/watch?v=EFWJIkT0LM8
Cours : Combine Altair with Dash for Fully Interactive Data Apps

Site @ sur Altair :
https://altair-viz.github.io/gallery/index.html

Site GitHub sur Altair :
https://github.com/altair-viz/dash-vega-components

Nouvelle librairie pour de nouveaux composants

Date : 01-11-2023
"""

import altair as alt     
from dash import Dash, Input, Output, callback, dcc, html
from vega_datasets import data # pour les données récupérées
import dash_vega_components as dvc # composants

# FRONT END -------------------------------------------------------------------

# Instanciation de la librairie
app = Dash()

# Configuration de la page @
app.layout = html.Div(
    [   
        # Titre principal de la page @
        html.H1("Altair Chart"),
        
        # Menu déroulant
        dcc.Dropdown(
            options=["All", "USA", "Europe", "Japan"], # Valeurs du composants
            value="All", # Valeur affichée par défaut
            id="origin-dropdown", # pour le callback
            ),
        
        # Composant de la librairie Altair (données vides)
        dvc.Vega(id="altair-chart", # pour le callback
                 opt={"renderer": "svg", # TODO
                      "actions": False, # TODO
                      }, 
                 spec={}, # Données vides
                 ),
    ]
)

# INTERACTION ENTRE COMPOSANTS ------------------------------------------------

# MAJ du nuage de points selon la valeur sélectionnée dans le menu déroulant
@callback(
    Output(component_id="altair-chart", # Sortie : Nuage de points
           component_property="spec"),
    Input(component_id="origin-dropdown", # Entrée : Menu déroulant
          component_property="value")
)
def display_altair_chart(origin):
    
    # Récupération des données à partir de la sous-librairie de vega_datasets
    source = data.cars()
    # print(source.head())

    # Filtre des données selon la valeur sélectionnée dans le menu déroulant
    if origin != "All":
        source = source[source["Origin"] == origin]

    # MAJ du nuage de points
    chart = (
        alt.Chart(source) # Données alimentées
        .mark_circle(size=60) # Taille des bulles
        .encode(
            x="Horsepower", # Axe des abscisses
            y="Miles_per_Gallon", # Axe des ordonnées
            color=alt.Color("Origin").scale(domain=[ # Couleurs des points
                "Europe", "Japan", "USA"]),
            tooltip=[ # Données affichées lors du survol du graphique
                "Name", "Origin", "Horsepower", "Miles_per_Gallon",
                ],
        )
        .interactive()
    )

    # source2 = px.data.medals_long()
    # # print(source2)
    # chart2 = alt.Chart(source2).mark_bar().encode(
    #     x='nation',
    #     y='count',
    #     color=alt.condition(
    #         alt.datum.count > 14,    # If the year is bigger than 14 this test returns True,
    #         alt.value('orange'),     # which sets the bar orange.
    #         alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    #     )
    # ).properties(width=400)

    return chart.to_dict()

if __name__ == "__main__":
    app.run(debug=True)
