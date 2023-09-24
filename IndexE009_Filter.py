"""
Lien : https://www.youtube.com/watch?v=stgbYj1QqsA&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=9
Cours : Dash DataTable Tips and Tricks

Multi-filtres sur la datatable à partir de menus déroulants et 
de barres de progression

Date : 24-09-23
"""

from dash import Dash, dash_table, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# DATASCIENCE -------------------------------------------------------------------

# Assignation du fichier .csv converti en DF pandas
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Récupération de certains champs
df = df[['continent', 'country', 'pop', 'lifeExp']]

# FRONT END -----------------------------------------------------------------------

# Instanciation de la librairie
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           )

# Configuration de la page Web
app.layout = dbc.Container([
    
    # Markdown : titre principale de la page @
    dcc.Markdown(
        '# DataTable - Trucs et astuces', 
        style={'textAlign':'center'},
                 ),

    # Label
    dbc.Label("Nombre de lignes à afficher dans la datatable"),
    
    # Menu déroulant sur le nombre de lignes à afficher dans la datatable
    row_drop := dcc.Dropdown(value=10, # Affichage par défaut
                             clearable=False, # Données non supprimables
                             style={'width':'35%'}, # Largeur du menu déroulant
                             options=[10, 25, 50, 100] # Valeurs du menu déroulant
                             ),

    # Datatable
    my_table := dash_table.DataTable(
        columns=[ # Configuration des colonnes
            {'name': 'Continent', 'id': 'continent', 'type': 'numeric'},
            {'name': 'Country', 'id': 'country', 'type': 'text'},
            {'name': 'Population', 'id': 'pop', 'type': 'numeric'},
            {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric'}
        ],
        data=df.to_dict('records'), # Récup de la DF en liste de dictionnaires
        filter_action='native', # Pagination active
        page_size=10, # Nombre de lignes max par page
        style_data={ # Mise en forme des colonnes
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        ),
    
    dbc.Row([
        
        dbc.Col([
            # Menu déroulant sur les continents
            continent_drop := dcc.Dropdown( # champ 'continent' de la DF
                [x for x in sorted(df.continent.unique())],
                )
        ], width=3),
        
        dbc.Col([     
            # Menu déroulant sur les pays
            country_drop := dcc.Dropdown( # champ 'country' de la DF
                [x for x in sorted(df.country.unique())], 
                multi=True, # Possibilité d'afficher plusieurs valeurs
                )
        ], width=3),
        
        
        dbc.Col([
            # Barre de progression sur la population
            pop_slider := dcc.Slider(
                0, # valeur min
                1_500_000_000, # valeur max
                5_000_000, # échelle d'écart
                marks={ # Marquage sur la barre
                    '1000000000':'1 milliard', 
                    '1500000000':'1.5 milliard'},
                value=0, # valeur par défaut affichée
                tooltip={ # Légendes à afficher
                    "placement": "bottom", # Valeur en bas de la barre
                    "always_visible": True # Toujours visible
                    },
                )
        ], width=3),
        
        dbc.Col([
            # Barre de progression sur l'espérance de vie
            lifeExp_slider := dcc.Slider(
                0, # valeur min
                100, # valeur max
                1, # échelle d'écart
                marks={'100':'100'}, # Marquage sur la barre
                value=20, # valeur par défaut affichée
                tooltip={ # Légendes à afficher
                    "placement": "bottom", # Valeur en bas de la barre
                    "always_visible": True # Toujours visible
                    },
                )
        ], width=3),

    ], justify="between", className='mt-3 mb-4'),

])

# FRONT END & BACK END -----------------------------------------------------

# Modification des données à afficher à la datatable selon les valeurs sélectionnées
# dans les menus déroulants et les barres de progression
@callback(
    Output(my_table, 'data'), # Sortie : datatable et données
    Output(my_table, 'page_size'), # Sortie : datatable et nbre de lignes par page
    Input(continent_drop, 'value'), # Entrée : menu déroulant sur les continents
    Input(country_drop, 'value'), # Entrée : menu déroulant sur les pays
    Input(pop_slider, 'value'), # Entrée : barre de progression sur la population
    Input(lifeExp_slider, 'value'), # Entrée : barre de prog sur l'espérance de vie
    Input(row_drop, 'value') # Entrée : menu déroulant nombre de lignes à afficher
)
def update_dropdown_options(cont_v, country_v, pop_v, life_v, row_v):
    
    # Copie de la DF
    dff = df.copy()

    # Si une valeur du menu déroulant sur les continents est affichée...
    if cont_v:
        # ... filtre sur le champ 'continent' de la DF copiée 
        dff = dff[dff.continent==cont_v]
    # Si une valeur du menu déroulant sur les pays est affichée...
    if country_v:
        # ... recoupement sur le champ 'country' de la DF copiée 
        dff = dff[dff.country.isin(country_v)]

    # Filtre sur le champ 'pop' selon la valeur sélectionnée dans la barre de 
    # progression sur la population avec une valeur n'excédant pas 1,5Md
    dff = dff[(dff['pop'] >= pop_v) & (dff['pop'] < 1_500_000_000)]
    
    # Filtre sur le champ 'lifeExp' selon la valeur sélectionnée dans la barre de 
    # progression sur l'espérance de vie avec une valeur n'excédant pas 100
    dff = dff[(dff['lifeExp'] >= life_v) & (dff['lifeExp'] < 100)]

    return (
        # MAJ de la DF
        dff.to_dict('records'),
        # Selon la valeur sélectionnée dans le 1er menu déroulant, nombre de lignes
        # à afficher dans la datatable
        row_v 
            )

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
