"""
Dans ce script, on intervient sur l'intéraction des widgets avec le callback,
en recourant cette fois-ci à des entrées multiples : 5 entrées et une sortie

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import pandas as pd
import plotly.graph_objs as go


# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

# Valeur unique pour le champ 'Indicator Name' de la DF
available_indicators = df['Indicator Name'].unique()

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Section de composants groupés
    html.Div([
        
        # 1ère sous-section
        html.Div([
            
            # Menu déroulant
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'),
            
            # Boutons d'option
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'})
            ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        # 2ème sous-section
        html.Div([
            
            # Menu déroulant
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'),
            
            # Bouton d'option
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'})
            ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]), 
     
    # Graphique
    dcc.Graph(id='indicator-graphic'),
    
    # Curseur
    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None)
])


# Le graphique se met à jour selon les composants sélectionnés, dont l'année
@app.callback(
    Output('indicator-graphic', 'figure'), # Une sortie : le graphique
    [Input('xaxis-column', 'value'), # Entrée 1 : Menu déroulant sous-section 1
     Input('yaxis-column', 'value'), # Entrée 2 : Menu déroulant sous-section 2
     Input('xaxis-type', 'value'), # Entrée 3 : Boutons d'option sous-section 1
     Input('yaxis-type', 'value'), # Entrée 4 : Boutons d'option sous-section 2
     Input('year--slider', 'value')]) # Entrée 5 : Curseur
def update_graph(xaxis_column_name, yaxis_column_name, # 5 arguments = 5 entrées
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return { # une variable en retour (le graphique) = 1 sortie
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
         'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
    