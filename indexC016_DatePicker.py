"""
Lien : https://www.youtube.com/watch?v=5uwxoxaPD8M&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=9
Cours : DatePickerRange - Python Dash Plotly

Documentation sur dcc.DatePickerRange (calendrier date début / date fin):
https://dash.plotly.com/dash-core-components/datepickerrange

Documentation sur plotly.express.density_mapbox (carte des densités):
https://plotly.com/python-api-reference/generated/plotly.express.density_mapbox.html#plotly.express.density_mapbox

Dans ce cours on apprend à utiliser un calendrier avec date début / date fin

Format des dates à afficher :
Saisie      Exemple         Description
YYYY        2014            4 or 2 digit year
YY          14              2 digit year
Y           -25             Year with any number of digits and sign
Q           1..4            Quarter of year. Sets month to first month in quarter
M MM        1..12           Month number
MMM MMMM    Jan..December   Month name
D DD        1..31           Day of month
Do          1st..31st       Day of month with ordinal
DDD DDDD    1..365          Day of year
X           1410715640.579  Unix timestamp
x           1410715640579   Unix ms timestamp

Date : 29-09-2023
"""

from datetime import datetime as dt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

# TRAITEMENTS EN DS ------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/Sidewalk_Caf__Licenses_and_Applications.csv")

# Changement du type du champ ci-après
df['SUBMIT_DATE'] = pd.to_datetime(df['SUBMIT_DATE'])

# Le champ désigné ci-après est l'index de la DF
df.set_index('SUBMIT_DATE', inplace=True)

print(df[:5][['BUSINESS_NAME', 'LATITUDE', 'LONGITUDE', 'APP_SQ_FT']])

# FRONT END ----------------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la sous-librairie Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div([
    
    # Calendrier date début / date fin
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID pour le callback
        calendar_orientation='horizontal',  # calendrier vertical ou horizontal
        day_size=39,  # taille du calendrier, par défaut c'est 39 pixels
        end_date_placeholder_text="Return",  # texte par défaut fin de date
        with_portal=False,  # True : affichage du calendrier au centre de l'écran
        first_day_of_week=0,  # 0 = 1er jour du calendrier : Dimanche
        is_RTL=False,  # Sens de direction du calendrier
        clearable=True,  # Valeurs sélectionnées supprimables
        number_of_months_shown=1,  # Nbre de mois affiché au calendrier
        min_date_allowed=dt(2018, 1, 1),  # Date min sélectionnable
        max_date_allowed=dt(2020, 6, 20),  # Date max sélectionnable
        initial_visible_month=dt(2020, 5, 1),  # Date par défaut affiché
        start_date=dt(2018, 8, 7).date(), # Date début affiché par défaut
        end_date=dt(2020, 5, 15).date(), # Date fin affiché par défaut
        display_format='MMM Do, YY', # Format des dates affichées
        month_format='MMMM, YYYY', # Format date de l'en-tête du calendrier
        minimum_nights=2, # Nombre mini de jours entre date début et date fin

        persistence=True, # Sauvegarde des données saisies dans les dates
        persisted_props=['start_date'], # Texte à conserver début date si reset
        persistence_type='session',  # session, local, ou memory -> défaut : 'local'

        # 'singledate' : une seule date modifiée met à jour le graphique
        # 'bothdates' : les deux dates doivent être modifiées pour MAJ du graphique
        updatemode='singledate' 
    ),

    # Titre
    html.H3("Sidewalk Café Licenses and Applications", 
            style={'textAlign': 'center'}),
    
    # Graphique vide
    dcc.Graph(id='mymap')
])

# INTERACTIONS ENTRE COMPOSANTS ---------------------------------------

# MAJ de la carte des densités selon les données saisies en date début / date fin
@callback(
    Output('mymap', 'figure'), # Sortie : graphique
    [Input('my-date-picker-range', 'start_date'), # Entrée : 
     Input('my-date-picker-range', 'end_date')] # Entrée : 
)
def update_output(start_date, end_date):
    # print("Start date: " + start_date)
    # print("End date: " + end_date)
    dff = df.loc[start_date:end_date]
    # print(dff[:5])

    # MAJ de la carte des densités
    fig = px.density_mapbox(dff, 
                            lat='LATITUDE', 
                            lon='LONGITUDE', 
                            z='APP_SQ_FT', 
                            radius=13, 
                            zoom=10, 
                            height=650,
                            center=dict(lat=40.751418, lon=-73.963878), 
                            mapbox_style="carto-positron",
                            hover_data={
                                'BUSINESS_NAME': True, 
                                'LATITUDE': False, 
                                'LONGITUDE': False,
                                'APP_SQ_FT': True})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)
