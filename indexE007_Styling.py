"""
Lien : https://www.youtube.com/watch?v=twHtUFR7rtw&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=7
Cours : DataTable Styling & Height -- Dash Plotly

Documentation - style sur les datatables :
https://dash.plotly.com/datatable/style

Documentation - propriétés des datatables :
https://dash.plotly.com/datatable/reference

Style et conditions -> ordres de priorité :
1. style_data_conditional
2. style_data
3. style_filter_conditional
4. style_filter
5. style_header_conditional
6. style_header
7. style_cell_conditional
8. style_cell

Date : 22-09-23
"""

from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict

app = Dash(__name__)

#-----------------------------------------------------------------------------
# Assignation d'une DF pandas à partir d'un OrderedDict de la librairie collections
data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)
df = pd.DataFrame(data)

# Configuration de la page @ avec une uniquement une datatable ---------------------

app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c, 
              'editable': (c == 'Humidity')} # Données modif pour cette colonne
             for c in df.columns],

#----------------------------------------------------------------
# Absence de ligne verticale séparatrice des colonnes
#----------------------------------------------------------------
    
    style_as_list_view=True,

#----------------------------------------------------------------
# Conditions sur les données
#----------------------------------------------------------------
    
    style_data_conditional=[ 
       
        # Couleur des lignes paires / impaires
        {
            'if': {'row_index': 'odd'}, # Si la ligne est impaire
            'backgroundColor': 'green' # Couleur de fond de la ligne
        },
        
        # Pour la ligne index 4 (5ème ligne), application des conditions ci-après
        {
        "if": {"row_index": 4},
        "backgroundColor": "purple", # Couleur de fond
        'color': 'white', # Couleur du texte
        "fontWeight": "bold" # Texte en gras
        },
        
        # Pour la colonne 'Temperature', application des conditions ci-après
        {
        'if': {'column_id': 'Temperature'},
        'backgroundColor': 'red', # Couleur de fond
        'color': 'white', # Couleur du texte
        },   
        
        # Pour la colonne 'Region', si la valeur = 'Montreal', alors...
        {
            'if': {
                'column_id': 'Region',
                'filter_query': '{Region} eq "Montreal"'
                },
            'backgroundColor': '#3D9970', # Couleur de fond
            'color': 'white', # Couleur du texte
        },
        
        # Pour la colonne 'Humidity', si la valeur = 20, alors...
        {
            'if': {
                'column_id': 'Humidity',
                'filter_query': '{Humidity} eq 20'
            },
            'backgroundColor': '#3D9970',
            'color': 'white',
        },
        
        # Pour la colonne 'Temperature', si la valeur > 3.9, alors...
        {
            'if': {
                'column_id': 'Temperature',
                'filter_query': '{Temperature} > 3.9'
            },
            'backgroundColor': '#3D9970',
            'color': 'white',
        },
        
        # Si la colonne est modifiable ('Humidity')
        # {
        #     'if': {'column_editable': True},
        #     'backgroundColor': 'rgb(30, 30, 30)', # Couleur de fond
        #     'color': 'white' # Couleur de texte
        # },
        ],

#----------------------------------------------------------------
# Style sur les données
#----------------------------------------------------------------

    style_data={ 'border': '1px solid red' }, # épaisseur et couleur des bordures

#----------------------------------------------------------------
# Conditions des en-têtes
#----------------------------------------------------------------

    style_header_conditional=[{  
            # Si la colonne est modifiable ('Humidity')
            'if': {'column_editable': True},
            'backgroundColor': 'rgb(30, 30, 30)', # Couleur de fond
            'color': 'white' # Couleur de texte
        }],

#----------------------------------------------------------------
# Style des en-têtes
#----------------------------------------------------------------
    
    style_header={ # 
        'backgroundColor': 'pink', # Couleur de fond
        'fontWeight': 'bold', # Texte en gras
        'border': '1px solid black' # Epaisseur des bordures
    },

#----------------------------------------------------------------
# Conditions sur les cellules
#----------------------------------------------------------------
    
    # Alignement du texte à gauche seulement pour les colonnes 'Date' et 'Region' 
    style_cell_conditional=[      
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],

#----------------------------------------------------------------
# Style des cellules
#----------------------------------------------------------------
    
    style_cell={
        'textAlign': 'left', # Alignement du texte à gauche
        'padding': '20px', # Hauteur des lignes
        'backgroundColor': 'rgb(50, 50, 50)', # Couleur de fond (sombre)
        'color': 'yellow', # Couleur du texte 
        # Texte non tronqué lorsque la largueur des cellules est fixée :
        'minWidth': 95, 'maxWidth': 95, 'width': 95, 
        },
    
#----------------------------------------------------------------
# En-têtes sur 2 lignes
#----------------------------------------------------------------
    # columns=[
    #     {"name": ["", "Year"], "id": "year"}, # ["", "Year"] = [ligne 1, ligne 2]
    #     {"name": ["City", "Montreal"], "id": "montreal"},
    #     {"name": ["City", "Toronto"], "id": "toronto"},
    #     {"name": ["City", "Ottawa"], "id": "ottawa"},
    #     {"name": ["City", "Vancouver"], "id": "vancouver"},
    #     {"name": ["Climate", "Temperature"], "id": "temp"},
    #     {"name": ["Climate", "Humidity"], "id": "humidity"},
    # ],
    # data=[
    #     {
    #         "year": i,
    #         "montreal": i * 10,
    #         "toronto": i * 100,
    #         "ottawa": i * -1,
    #         "vancouver": i * -10,
    #         "temp": i * -100,
    #         "humidity": i * 5,
    #     }
    #     for i in range(10)
    # ],
    # merge_duplicate_headers=True, # Fusion des entêtes en 1ère ligne

)

if __name__ == '__main__':
    app.run_server(debug=True)
