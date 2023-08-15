"""
Lien : https://www.youtube.com/watch?v=hSPmj7mK6ng
Cours : Introduction to Dash Plotly - Data Visualization in Python

Lancement du fichier python dans le terminal :
python indexB001_Intro.py 

Avec dans le script : app.run_server(debug=False) et non True, 
sinon la page @ ne s'affiche pas

Date : 15-08-2023
"""
import pandas as pd
import plotly.express as px

from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Instanciation de la librairie
app = Dash(__name__)

# Importation du fichier .csv en pandas
df = pd.read_csv('data/intro_bees.csv')

# TCD de la DF
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[[
    'Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
# print(df.head())

# Configuration de la page @
app.layout = html.Div([
    
    # Titre principal de la page
    html.H1("Page web d'un tableau de bord avec Dash",
            style={'text-align':'center'}),
    
    # Menu déroulant
    dcc.Dropdown(id='slct_year',
                 options=[
                     {'label':'2015', 'value':2015},
                     {'label':'2016', 'value':2016},
                     {'label':'2017', 'value':2017},
                     {'label':'2018', 'value':2018},
                     {'label':'2019', 'value':2019},],
                 multi=False, # Affichage multiple
                 value=2015, # Affichage par défaut
                 style={'width':'40%'},),
    
    # Saut de ligne
    html.Br(),
    
    # Texte
    html.Div(id='output_container', 
             children=[]), # Texte vide
    
    # Saut de ligne
    html.Br(),
    
    # Graphique
    dcc.Graph(id='my_bee_map',
              figure={}), # Graphique vide
])

# Liens entre widgets
@app.callback(
    [Output( # Sortie : texte
        component_id='output_container',
        component_property='children'),
     Output( # Sortie : graphique
        component_id='my_bee_map',
        component_property='figure'),
     Input( # Entrée : menu déroulant
        component_id='slct_year',
        component_property='value')])
def update_graph(option_slctd): # un argument en paramètre = une entrée (input)
   
    # Intervention sur la DF
    dff = df.copy() # Copie de la DF
    dff = dff[dff['Year'] == option_slctd] # Filtre DF : Année sélectionnée
    dff = dff[dff['Affected by'] == 'Varroa_mites'] # Autre filtre de la DF
    
    # MAJ du texte
    container = f"Année choisie par l'utilisateur : {option_slctd}"
    
    # MAJ du graphique
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Imacted': '% of Bee Colonies'},
        template='plotly_dark',)
    
    return container, fig # deux variables en return = deux sorties (output)

if __name__ == '__main__':
    app.run_server(debug=False)
