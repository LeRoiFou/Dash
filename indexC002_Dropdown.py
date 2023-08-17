"""
Lien : https://www.youtube.com/watch?v=UYH_dNSX1DM&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=1
Cours : Dropdown Selector- Python Dash Plotly

Date : 17-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import pandas as pd
import plotly.express as px

#---------------------------------------------------------------
# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/Urban_Park_Ranger_Animal_Condition.csv")  
# print(df.columns)

#---------------------------------------------------------------
# Instanciation de la librairie
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div(children=[

    # 1ère section
    html.Div([
        
        # Graphique vide
        dcc.Graph(id='our_graph')
        
        ],className='nine columns'),
    
    # 2ème section
    html.Div([

        # Saut de ligne
        html.Br(),
        
        # Texte vide
        html.Div(children='', 
                 id='output_data'),
        
        # Saut de ligne
        html.Br(),

        # ...
        html.Label(['Choose column:'],
                   style={'font-weight': 'bold', "text-align": "center"}),

        # Menu déroulant
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                     {'label': 'Species', 'value': 'Animal Class'},
                     {'label': 'Final Ranger Action', 'value': 'Final Ranger Action'},
                     {'label': 'Age', 'value': 'Age', 'disabled':True}, # désactivé
                     {'label': 'Animal Condition', 'value': 'Animal Condition'},
                     {'label': 'Borough', 'value': 'Borough'},
                     {'label': 'Species Status', 'value': 'Species Status'}],
            optionHeight=35, # Espace entre les données
            value='Borough', # Valeur par défaut
            disabled=False, # Non désactivé
            multi=False, # Sélection multiple 
            searchable=True, # Recherche F - possibilité de saisir
            placeholder='Please select...', # texte si rien est sélectionné
            clearable=True, # Possibilité de ne rien afficher par défaut             
            style={'width':"100%"}, # Largeur du menu déroulant
            # className='select_box', # Personnalisation du widget... (00:15:00)
            ),             
    
    ],className='three columns'),
])

#---------------------------------------------------------------
# MAJ du camembert selon le choix sélectionné dans le menu déroulant : 
# Le graphique va récupérer le champ filtré de la DF à partir du menu déroulant
@app.callback(
    Output( # Sortie : graphique
        component_id='our_graph', component_property='figure'),
    [Input( # entrée : menu déroulant
        component_id='my_dropdown', component_property='value')])
def build_graph(column_chosen): # un argument = une entrée du menu déroulant
    dff=df # copie de la DF
    fig = px.pie(dff, names=column_chosen)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'NYC Calls for Animal Rescue',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig  # une variable = une sortie de la MAJ du graphique

#---------------------------------------------------------------
# MAJ du texte selon le choix sélectionné dans le menu déroulant : 
# Le texte va afficher l'option choisie dans le menu déroulant
@app.callback(
    Output( # La sortie : le texte vide
        component_id='output_data', component_property='children'),
    [Input( # l'entrée : le menu déroulant
        component_id='my_dropdown', component_property='value')])
def build_graph(data_chosen): # un argument = une entrée du menu déroulant
    return f'Valeur sélectionné dans le menu déroulant : " {data_chosen} "'

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
