"""
Lien : https://www.youtube.com/watch?v=Kr94sFOWUMg&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=6
Cours : Line Plot (Dropdown) - Dash Python

Documentation sur dcc.Dropdown :
https://dash.plotly.com/dash-core-components/dropdown

Documentation sur plotly.express.line :
https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line

Graphique linéaire : MAJ selon les valeurs sélectionnées dans les menus déroulants

Date : 15-10-23
"""

import pandas as pd   
import plotly.express as px
from dash import Dash, html, dcc, Output, Input, callback
import warnings

# DS ---------------------------------------------------------------------------

# Récupération du ficheir .csv converti en DF pandas
df = pd.read_csv("assets/DOHMH_New_York_City_Restaurant_Inspection_Results_20231015.csv")

# Conversion du champ 'INSPECTION DATE' en datetime
df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])

# TCD sur les champs ci-après: moyenne pour le champ 'SCORE'
df = df.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','CAMIS']
                , as_index=False)['SCORE'].mean()

# Champ 'INSPECTION DATE' constituant l'index de la DF
df = df.set_index('INSPECTION DATE')

# Filtre sur les lignes ci-après
df = df.loc['2016-01-01':'2019-12-31']

# TCD : regroupement par le champ 'CUISINE DESCRIPTION' avec une moyenne pour
# le champ 'SCORE' par mois (freq = "M")
df = df.groupby([pd.Grouper(freq="M"),'CUISINE DESCRIPTION']
                )['SCORE'].mean().reset_index()
# print (df[:5])

# FRONT END ---------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([

    html.Div([
        
        # Graphique
        dcc.Graph(
            id='our_graph', # pour le callback
            )
    ],className='nine columns'),

    html.Div([

        # Saut de ligne
        html.Br(),
        
        # Titre rattaché aux menus déroulants
        html.Label(
            ['Choose 3 Cuisines to Compare:'], # Titre
            style={'font-weight': 'bold', "text-align": "center"}, # Forme
            ),
        
        # Menu déroulant n° 1
        dcc.Dropdown(
            id='cuisine_one', # pour le callback
            options=[{'label':x, 'value':x} # valeurs pour le composant
                     for x in df.sort_values('CUISINE DESCRIPTION')
                     ['CUISINE DESCRIPTION'].unique()],
            value='African', # affichage par défaut
            multi=False, # un seul affichage
            disabled=False, # non verrouillé
            clearable=True, # possibilité de supprimer la valeur affichée
            searchable=True, # recherche possible de la valeur souhaitée
            placeholder='Choose Cuisine...', # texte affiché si absence valeur
            className='form-dropdown', # fichier CSS dans le répertoire 'assets'
            style={'width':"90%"}, # largeur du menu déroulant
            persistence='string', # valeurs du menu déroulant : str ici
            persistence_type='memory', # / local / session
            ),

        # Menu déroulant n° 2
        dcc.Dropdown(
            id='cuisine_two', # pour le callback
            options=[{'label':x, 'value':x} # valeurs pour le composant
                     for x in df.sort_values('CUISINE DESCRIPTION')
                     ['CUISINE DESCRIPTION'].unique()],
            value='Creole', # affichage par défaut
            multi=False, # un seul affichage
            clearable=False, # pas de possibilité de supprimer la valeur affichée
            persistence='string', # valeurs du menu déroulant : str ici
            persistence_type='session', # / local / session
            ),

        # Menu déroulant n° 3
        dcc.Dropdown(
            id='cuisine_three', # pour le callback
            options=[{'label':x, 'value':x}  # valeurs pour le composant
                     for x in df.sort_values('CUISINE DESCRIPTION')
                     ['CUISINE DESCRIPTION'].unique()],
            value='Coffee/Tea', # affichage par défaut
            multi=False, # un seul affichage
            clearable=False, # pas de possibilité de supprimer la valeur affichée
            persistence='string', # valeurs du menu déroulant : str ici
            persistence_type='local', # / local / session
            ),

    ],className='three columns'),

])

# INTERACTIONS ENTRE COMPOSANTS ----------------------------------------------

# MAJ du graphique linéaire selon les valeurs sélectionnées dans chacun des 
# menus déroulants
@callback(
    Output('our_graph','figure'), # Sortie : graphique
    [Input('cuisine_one','value'), # Entrée : menu déroulant n° 1
     Input('cuisine_two','value'), # Entrée : menu déroulant n° 2
     Input('cuisine_three','value'), # Entrée : menu déroulant n° 3 
     ]
)
def build_graph(first_cuisine, second_cuisine, third_cuisine):
    
    # Filtre sur la DF selon les valeurs sélectionnées dans les menus déroulants
    dff=df[(df['CUISINE DESCRIPTION']==first_cuisine)|
           (df['CUISINE DESCRIPTION']==second_cuisine)|
           (df['CUISINE DESCRIPTION']==third_cuisine)]
    # print(dff[:5])

    # MAJ du graphique linéaire
    fig = px.line(
        dff, # Récupération des données de la DF filtrée
        x="INSPECTION DATE", # Champ pour l'axe des abscisses
        y="SCORE", # Champ pour l'axe des ordonnées
        color='CUISINE DESCRIPTION',  # Couleur selon ce champ
        height=600, # Hauteur du graphique
        )
    
    fig.update_layout(
        yaxis={'title':'NEGATIVE POINT'}, # Titre modifié pour l'axe des ordonnées
        title={'text':'Restaurant Inspections in NYC', # Titre du graphique
               'font':{'size':28},'x':0.5, # Forme
               'xanchor':'center'}, # Centré
        )
    return fig


if __name__ == '__main__':
    
    # Suppression du message d'avertissement dans le terminal
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    app.run_server(debug=True)
  