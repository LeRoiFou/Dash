"""
Lien : https://www.youtube.com/watch?v=stgbYj1QqsA&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=9
Cours : Dash DataTable Tips and Tricks

Documentation pour masquer les colonnes de la datatable au regard des 
dimensions adaptées à la fenêtre de l'ordinateur : pour que ça 
fonctionne, il faut remettre à jour la page @ (touche F5)
... utilie pour les téléphones portables ?
https://community.plotly.com/t/how-to-hide-datatable-columns-based-on-screen-size/60582/3?u=adamschroeder

Documentation sur le composant dcc.Location :
https://dash.plotly.com/dash-core-components/location

Date : 24-09-23
"""

from dash import Dash, dash_table, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# DATASCIENCE -------------------------------------------------------------------

# Assignation du fichier .csv converti en DF pandas
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Récupération de certains champs
df = df[['continent', 'country', 'pop', 'lifeExp']]

# FRONT END -----------------------------------------------------------------------

# Instancition de la librairie
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           )

# Instanciation de la librairie
app.layout = dbc.Container([
    
    # Markdown : titre principale de la page @
    dcc.Markdown(
        '# Hide Columns per Screen Size', 
        style={'textAlign':'center'},
        ),

    # Datatable
    my_table := dash_table.DataTable(
        id='table',
        columns=[ # Configuration des colonnes
            {'name': 'Continent', 'id': 'continent', 'type': 'numeric'},
            {'name': 'Country', 'id': 'country', 'type': 'text'},
            {'name': 'Population', 'id': 'pop', 'type': 'numeric'},
            {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric'}
        ],
        data=df.to_dict('records'), # Récup de la DF en liste de dictionnaires
        page_size=10, # Nombre de lignes max par page
        style_data={ # Mise en forme des colonnes
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    ),
    
    # Composant barre d'adresse navigateur @
    dcc.Location(id='_pages_plugin_location')
])

# FRONT END & BACK END -----------------------------------------------------

# Callback atypique : 
# -> Les paramètres du callback prennent en compte un langage qui n'est pas Python
# -> Pas de fonction appelée au callback
# À une certaine taille de la fenêtre (750 pixels), afficher uniquement les colonnes
# 'continent' et 'lifeExp' de la datatable, en mettant à jour la barre d'adresse
# du navigateur @
app.clientside_callback(
    """
        function(href) {
            if (window.innerWidth < 750) {
                return ['continent', 'lifeExp']
            }
            return []
        }
    """,
    Output('table', 'hidden_columns'), # Sortie : datatable
    Input('_pages_plugin_location', 'href') # Entrée : # Barre d'adresse navigateur @
)

if __name__ == '__main__':
    app.run_server(debug=True, 
                #    port=8003
                   )
