"""
Lien : https://www.youtube.com/watch?v=amRFPjSgEnk&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=7
Cours : Checklist - Python Dash Plotly

Dans ce cours on a recours aux cases à cocher qui permettent de mettre à jour 
un graphique

Documentation sur le composant dcc.Checklist
https://dash.plotly.com/dash-core-components/checklist

Date : 26-09-2023
"""

import pandas as pd     
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# DS --------------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/Urban_Park_Ranger_Animal_Condition_Response.csv")

# Filtre sur la DF
df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Nouveau champ de la DF récupérant uniquement le mois du champ 
# 'Date and Time of initial call'
df['Month Call Made'] = pd.to_datetime(df['Date and Time of initial call'])
df['Month Call Made'] = df['Month Call Made'].dt.strftime('%m')

# Trie croissant
df.sort_values('Month Call Made', inplace=True)

# Remplacement des valeurs du champ suivant
df['Month Call Made'] = df['Month Call Made'].replace(
    {"01":"January","02":"February","03":"March",
     "04":"April","05":"May","06":"June",
     "07":"July","08":"August","09":"September",
     "10":"October","11":"November","12":"December",})

# Modification du nom du champ
df['Amount of Animals'] = df['# of Animals']

# FRONT END --------------------------------------------------------------------

# Intanciation de la librairie
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([

        
        html.Div([
            
            # Un tout petit titre, tout petit tout petit tout petit !
            html.Pre(
                children= "NYC Calls for Animal Rescue",
                style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),

        html.Div([
            
            # Cases à cocher
            dcc.Checklist(
                id='my_checklist',
                
                options=[ # Autant d'options à cocher que de valeurs dans le champ
                          # 'Month Call Made' dans la DF (soit 12 valeurs)
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['Month Call Made'].unique()
                         ],
                value=['January','July','December'], # Valeurs par défaut cochées    
                style={'display':'flex'}, # Cases à cocher flexibles     
                inputStyle={'cursor':'pointer'}, # pointeur de la souris sur la case      
                labelStyle={'background':'#A5D6A7', # mise en forme
                            'padding':'0.5rem 1rem',
                            'border-radius':'0.5rem'},
                
                # stores user's changes to dropdown in memory 
                # (I go over this in detail in Dropdown video: 
                # https://youtu.be/UYH_dNSX1DM)
                # persistence='', 
                
                # stores user's changes to dropdown in memory 
                # (I go over this in detail in Dropdown video: 
                # https://youtu.be/UYH_dNSX1DM)
                # persistence_type='',                   
            ),
        ]),

        html.Div([
            
            # Graphique vide
            dcc.Graph(id='the_graph')
    ]),

])

# FRONT END & BACK END ------------------------------------------------------------

# MAJ du graphique selon les cases cochées
@app.callback(
    Output( # Sortie : graphique
        component_id='the_graph', 
        component_property='figure'),
    [Input( # Entrée : cases à cocher
        component_id='my_checklist', 
        component_property='value')]
)
def update_graph(options_chosen):

    # Recoupemnt de la DF en fonction de la case cochée
    dff = df[df['Month Call Made'].isin(options_chosen)]
    print(dff['Month Call Made'].unique())

    # MAJ du diagramme en camembert
    piechart=px.pie(
            data_frame=dff,
            values='Amount of Animals',
            names='Month Call Made',
            )

    return piechart

#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
