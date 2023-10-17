"""
Lien : https://www.youtube.com/watch?v=DCHkv3x3Vs8&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=8
Cours : Scatter Plot (RangeSlider) - Python Dash Plotly

Documentation sur dcc.RangeSlider (curseur par intervalle) :
https://dash.plotly.com/dash-core-components/rangeslider

Documentation sur plotly.express.scatter (nuage de points) :
https://plotly.com/python-api-reference/generated/plotly.express.scatter.html

MAJ d'un nuage de points à partir d'un curseur à intervalles

Date : 17-10-23
"""

from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/suicide_rates.csv")

# CONFIGURATION DES COMPOSANTS ---------------------------------------------

# Pour le curseur à intervalles : valeurs
mark_values = {1985:'1985',1988:'1988',1991:'1991',1994:'1994',
               1997:'1997',2000:'2000',2003:'2003',2006:'2006',
               2009:'2009',2012:'2012',2015:'2015',2016:'2016'}

# FRONT END ----------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
        html.Div([
            
            # Texte de la page @ (texte tout pourri)
            html.Pre(
                children= "Suicide Rates 1985-2016",
                style={"text-align": "center", 
                       "font-size":"100%", 
                       "color":"black",},
                )
        ]),

        # Graphique (vide)
        html.Div([
            dcc.Graph(
                id='the_graph', # pour le callback
                )
        ]),

        html.Div([
            
            # Curseur à intervalles
            dcc.RangeSlider(
                id='the_year', # pour le callback
                min=1985, # valeur minimum
                max=2016, # valeur maximum
                value=[1985,1988], # plage d'intervalle sélectionnée par défaut
                marks=mark_values, # valeur (voir configuration des composants)
                step=None, # pas d'échelles que celles appliquées pour les valeurs
                )
        ],style={"width": "70%", 
                 "position":"absolute",
                 "left":"5%",},
        )

])

#INTERACTION DES COMPOSANTS ----------------------------------------------------

@callback(
    Output('the_graph','figure'), # Sortie : graphique
    [Input('the_year','value')] # Entrée : curseur à intervalles
)
def update_graph(years_chosen):
    
    # years_chosen est une liste de données numériques
    # print(years_chosen)

    # Filtre sur le champ 'year' de la DF selon les années choisies dans le curseur
    # à intervalles (récupération de l'année la plus ancienne [1er composant] et
    # l'année la plus récente [2ème composant])
    dff=df[(df['year']>=years_chosen[0]) &
           (df['year']<=years_chosen[1])]
    
    # TCD avec le champ 'country' : moyenne pour les champs "suicides/100k pop" et
    # "gdp_per_capita ($)" (valeurs pour les axes x et y du graphique)
    dff=dff.groupby(["country"], as_index=False)[
        ["suicides/100k pop", "gdp_per_capita ($)"]].mean()
    
    # print (dff[:3])

    # MAJ du graphique (nuage de points)
    scatterplot = px.scatter(
        data_frame=dff, # DF filtrée et en TCD
        x="suicides/100k pop", # Valeurs pour l'axe des abscisses
        y="gdp_per_capita ($)", # Valeurs pour l'axe des ordonnées
        hover_data=['country'], # Données sup affichées en survolement du graph
        text="country", # Textes affichés dans le graph (ici nom des pays)
        height=550, # Hauteur du graphique
    )
    scatterplot.update_traces(
        textposition='top center', # Position des textes affichés dans le graph
        )

    return scatterplot

if __name__ == '__main__':
    app.run_server(debug=True)
