"""
Lien : https://www.youtube.com/watch?v=dLykSQNIM1E&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=14
Cours : Sharing Data between Dash Callbacks

Documentation sur le composant dcc.Store :
https://dash.plotly.com/dash-core-components/store

Documentation sur le partage de données avec les callbacks
https://dash.plotly.com/sharing-data-between-callbacks

Dans ce cours on apprend à utiliser le dcc.store permettant de stocker des données 
jusqu'à une certainne taille : 
"Il est généralement prudent de stocker jusqu'à 2 Mo dans la plupart des 
environnements, et de 5 à 10 Mo dans la plupart des applications de bureau"

On apprend également l'intérêt de l'instruction storage_type dans ce composant :
-> memory : dès rafraîchissement de la page @, les données sauvegardées dans ce
composant sont effacées ;
-> session : dès qu'on quitte la page @, les données sauvegardées dans ce
composant sont effacées ;
-> local : les données sauvegardées dans ce composant ne sont jamais effacées

Date : 04-10-23
"""
from dash import Dash, html, dcc, Output, Input, callback, dash_table
import pandas as pd
import plotly.express as px

# FRONT END ------------------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la sous-librairie Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div([
    
    # Titre principal
    html.H1(
        'Sharing Data between callbacks', 
        style={'textAlign':'center'},
            ),
    
    html.Div([
        
        # Menu déroulant
        dcc.Dropdown(
            id='data-set-chosen', # pour le callback
            multi=False, # affichage d'une seule valeur
            value='gapminder', # valeur par défaut affichée
            options=[{'label':'Country Data', 'value':'gapminder'}, # valeurs
                     {'label':'Restaurant Tips', 'value':'tips'},
                     {'label':'Flowers', 'value':'iris'}]),
        ], 
             className='row', 
             style={'width':'50%'}),

    html.Div([
        
        # Graphique vide
        html.Div(id='graph1', 
                 children=[], 
                 className='six columns',
                 ),
    ], className='row'),

    html.Div([
        
        # Zone vide pour la datatable
        html.Div(
            id='table-placeholder', 
            children=[],
            )
    ], className='row'),

    # Stockage des données
    dcc.Store(
        id='store-data', 
        data=[], 
        storage_type='memory') # 'local' or 'session'
])

# INTERACTIONS ENTRE COMPOSANTS --------------------------------------------

# Selon la valeur sélectionnée dans le menu déroulant, récupération des données
# dans la sous-librairie plotly express pour les stocker dans le composant dcc.store
# sous la forme d'une liste de dictionnaires
@callback(
    Output('store-data', 'data'), # Sortie : stockage des données
    Input('data-set-chosen', 'value') # Entrée : menu déroulant
)
def store_data(value):
    
    if value == 'gapminder':
        dataset = px.data.gapminder()
    elif value == 'tips':
        dataset = px.data.tips()
    elif value == 'iris':
        dataset = px.data.iris()
    
    # Option n° 1 : sauvegarde sous une liste de dictionnaires
    return dataset.to_dict('records')

    # Option n° 2 : sauvegarde sous format JSON
    # return dataset.to_json(orient='split')

# MAJ du graphique selon les données récupérées dans le composant dcc.store
@callback(
    Output('graph1', 'children'), # Sortie : graphique
    Input('store-data', 'data') # Entrée : stockage des données
)
def create_graph1(data):
    
    print(type(data)) # Liste de dictionnaires
    
    # Option n° 1 : conversion de la liste de dictionnaires en DF pandas
    dff = pd.DataFrame(data)
    
    # Option n° 2 : conversion du fichier JSON en DF pandas
    # dff = pd.read_json(data, orient='split')
    
    print(dff.head())
    print(type(dff))
    
    # Selon les données stockées dans le composant dcc.store, MAJ du graphique
    
    # Graphique en ligne
    if 'country' in dff.columns:
        fig1 = px.line(dff, x='year', y='lifeExp', color='continent')
        return dcc.Graph(figure=fig1)

    # Diagramme en barre
    elif 'total_bill' in dff.columns:
        fig2 = px.bar(dff, x='day', y='tip', color='sex')
        return dcc.Graph(figure=fig2)

    # Nuage de points
    elif 'sepal_length' in dff.columns:
        fig3 = px.scatter(dff, x='sepal_width', y='petal_width', color='species')
        return dcc.Graph(figure=fig3)


@callback(
    Output('table-placeholder', 'children'), # Sortie : datatable
    Input('store-data', 'data') # Entrée : stockage des données
)
def create_graph1(data):
    
    # Option n° 1 : conversion de la liste de dictionnaires en DF pandas
    dff = pd.DataFrame(data)
    
    # Option n° 2 : conversion du fichier JSON en DF pandas
    # dff = pd.read_json(data, orient='split')
    
    # MAJ de la datatable selon les données récupérées dans le composant dcc.STORE
    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.to_dict('records')
    )
    return my_table

if __name__ == '__main__':
    app.run_server(debug=True)
