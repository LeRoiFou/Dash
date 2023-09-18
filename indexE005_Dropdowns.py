"""
Lien : https://www.youtube.com/watch?v=kng-EKQGpYE&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=5
Cours : Dropdowns inside DataTable -- Dash Plotly

Menu déroulant dans une datatable 🤣🤣🤣

Date : 18-09-2023
"""

#code taken from https://dash.plot.ly/datatable/dropdowns
from dash import Dash, html, dash_table
import pandas as pd
from collections import OrderedDict

# We will cover all 3 DataTable Dropdown options:
# 1. per-Column Dropdowns (you choose column)
# 2. per-Row Dropdowns (starts from 1st row to as many rows as you want)
# 3. per-Row-Col Dropdowns (conditional, you choose which row/column)


app = Dash(__name__)
#-------------------------------------------------------------------
# 1. DataTable avec un menu déroulant par cellule pour certains champs

# Instanciation d'une DF sous pandas
df = pd.DataFrame(OrderedDict([
    ('climate', ['Sunny', 'Snowy', 'Sunny', 'Rainy']),
    ('temperature', [13, 43, 50, 30]),
    ('city', ['NYC', 'Montreal', 'Miami', 'NYC'])
]))

# Configuration de la page @
app.layout = html.Div([
    
    # Datatable
    dash_table.DataTable(
        id='table-dropdown',
        data=df.to_dict('records'),
        columns=[
            {'id': 'climate', 'name': 'climate', 'presentation': 'dropdown'},
            {'id': 'temperature', 'name': 'temperature'},
            {'id': 'city', 'name': 'city', 'presentation': 'dropdown'},
        ],
        editable=True,  # Modifiable
        dropdown={ # Menu déroulant dans la datatable
            'climate': {  # Champ concerné : 'climate'
                'options': [  # Toutes les valeurs de ce champ dans une cellule
                    {'label': i, 'value': i}
                    for i in df['climate'].unique()
                ],

                'clearable':True # Suppression de la valeur affichée
            },
            'city': { # Champ concerné : 'city'
                'options':[ # Toutes les valeurs dans ce champ dans une cellule
                    {'label': 'NYC', 'value': 'NYC'},
                    {'label': 'Miami', 'value': 'Miami'},
                    {'label': 'Montreal', 'value': 'Montreal'}
                ],

                'clearable':False
            }
        }
    ),
])


#-------------------------------------------------------------------
# 2. DataTable avec un menu déroulant par certains champs et pour certaines lignes

# # Instanciation d'une DF sous pandas
# df = pd.DataFrame(OrderedDict([
#     ('climate', ['Sunny', 'Snowy', 'Sunny', 'Rainy']),
#     ('temperature', [13, 43, 50, 30]),
#     ('city', ['NYC', 'Montreal', 'Miami', 'NYC'])
# ]))

# # Configuration de la page @
# app.layout = html.Div([
    
#     # Datatable
#     dash_table.DataTable(
#         id='table-dropdown',
#         data=df.to_dict('records'),
#         columns=[
#             {'id': 'climate', 'name': 'climate', 'presentation': 'dropdown'},
#             {'id': 'temperature', 'name': 'temperature'},
#             {'id': 'city', 'name': 'city', 'presentation': 'dropdown'},
#         ],
#         editable=True, # Modifiable
        
#         # Par compréhension de liste cette fois-ci : 
#         # ne porte que sur les 2 premières lignes                      
#         dropdown_data=[{ 
#             'climate': { # Champ concerné : 'climate'
#                 'options': [ # Toutes les valeurs de ce champ dans une cellule
#                     {'label': i, 'value': i}
#                     for i in df['climate'].unique()
#                 ],

#                 'clearable':True # Suppression de la valeur affichée
#             },

#             'city': { # Champ concerné : 'city'
#                 'options': [ # Toutes les valeurs de ce champ dans une cellule
#                     {'label': i, 'value': i}
#                     for i in df['city'].unique()
#                 ],

#                 'clearable':True # Suppression de la valeur affichée
#             },
#         } for x in range(2) # uniquement les deux premières lignes
#         ],

#     ),
# ])


#-------------------------------------------------------------------
# 3. DataTable avec un menu déroulant à afficher à certaines conditions

# # Instanciation d'une DF sous pandas
# df = pd.DataFrame(OrderedDict([
#     ('City', ['NYC', 'Montreal', 'Los Angeles']),
#     ('Neighborhood', ['Brooklyn', 'Mile End', 'Venice']),
#     ('Temperature (F)', [70, 60, 90]),
# ]))

# # Configuration de la page @
# app.layout = html.Div([
    
#     # Datatable
#     dash_table.DataTable(
#         id='dropdown_per_row',
#         data=df.to_dict('records'),
#         columns=[
#             {'id': 'City', 'name': 'City'},
#             {'id': 'Neighborhood', 'name': 'Neighborhood', 'presentation': 'dropdown'},
#             {'id': 'Temperature (F)', 'name': 'Temperature (F)'}
#         ],
#         editable=True, # Modifiable
                                    
#         dropdown_conditional=[{ 
                               
#             'if': {
#                  # Si pour le champ 'City' la valeur est égale à 'NYC', alors 
#                  # pour le champ 'Neighborhood'....
#                 'column_id': 'Neighborhood',      
#                 'filter_query': '{City} eq "NYC"'  
#             }, # ... affichage du menu suivant
#             'options': [
#                             {'label': i, 'value': i}
#                             for i in [
#                                 'Brooklyn',
#                                 'Queens',
#                                 'Staten Island'
#                             ]
#                         ],
#             'clearable':True # Suppression de la valeur affichée
#         },

#         {   
#             'if': {
#                 # Si pour le champ 'City' la valeur est égale à 'Los Angeles', alors 
#                 # pour le champ 'Neighborhood'....
#                 'column_id': 'Neighborhood',
#                 'filter_query': '{City} eq "Los Angeles"'
#             },
#             # ... affichage du menu suivant
#             'options': [
#                             {'label': i, 'value': i}
#                             for i in [
#                                 'Venice',
#                                 'Hollywood',
#                                 'Los Feliz'
#                             ]
#                         ],
#             'clearable':True # Suppression de la valeur affichée
#         }]
#     ),

# ])


if __name__ == '__main__':
    app.run_server(debug=True)