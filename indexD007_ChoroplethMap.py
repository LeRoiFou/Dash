"""
Lien : https://www.youtube.com/watch?v=WBiMeRD5yXk&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=9
Cours : Choropleth Map (Submit Button) - Python Dash Plotly

Documentation suR dcc.Input :
https://dash.plotly.com/dash-core-components/input

Documentation sur Button Examples and Reference : 
https://dash.plotly.com/dash-html-components/button

Documentation sur plotly.express.choropleth : 
https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html

Documentation sur Built-in Continuous Color Scales in Python : 
https://plotly.com/python/builtin-colorscales/

Documentation sur Basic Dash Callbacks : 
https://dash.plotly.com/basic-callbacks

MAJ d'une carte graphique à partir d'une zone de saisie des données numériques
(années)

Date : 18-07-23
"""

import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate


# FRONT END -------------------------------------------------------

# Mise en forme de la page @
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Instanciation de la sous-librairie Dash
app = Dash(__name__, 
           external_stylesheets=external_stylesheets,
           )

# Configuration de la page @
app.layout = html.Div([

    html.Div([
        
        # Graphique (vide)
        dcc.Graph(
            id='the_graph', # pour le callback
            )
    ]),

    html.Div([
        
        # Zone de saisie
        dcc.Input(
            id='input_state', # pour le callback
            type='number', # saisie obligatoirement en numérique
            inputMode='numeric', # saisie obligatoirement en numérique
            value=2007, # valeur affichée par défaut
            max=2007, # valeur max
            min=1952, # valeur min
            step=5, # échelle
            required=True, # Cadre de couleur rouge si absence de saisie
            ),
        
        # Bouton
        html.Button(
            id='submit_button', # pour le callback
            n_clicks=0, # valeur par défaut (pas de clique préalable)
            children='Submit', # Texte
                    ),
        
        # Zone de texte (vide)
        html.Div(
            id='output_state', # pour le callback
            ),
        
    ],style={'text-align': 'center'}),

])

# INTERACTION ENTRE LES WIDGETS
@callback(
    [Output('output_state', 'children'), # Sortie : Zone de texte
    Output('the_graph', 'figure')], # Sortie : Graphique
    [Input('submit_button', 'n_clicks')], # Entrée : Bouton
    [State('input_state', 'value')] # Entrée : Zone de saisie
)
def update_output(num_clicks, val_selected):
    
    # Si aucune valeur n'est affichée dans la zone de saisie...
    if val_selected is None:
        
        # Levée de l'exception avec la sous-librairie PreventUpdate
        raise PreventUpdate
    
    # Si une valeur est affichée dans la zone de saisie...
    else:
        
        # Filtre de la DF selon l'année saisie dans la zone de saisie
        df = px.data.gapminder().query(f"year=={val_selected}")
        # print(df.head(3))

        # MAJ du graphique (carte)
        fig = px.choropleth(
            df, 
            locations="iso_alpha", # Champ de la DFS
            color="lifeExp", # Couleur par rapport à ce champ
            hover_name="country", # Pays en survolant la carte
            projection='natural earth', # Contour de la carte (ici ovale)
            title='Life Expectancy by Year', # Titre du graphique
            color_continuous_scale=px.colors.sequential.Plasma, # Couleurs graph
            )

        # MAJ du titre du graphique
        fig.update_layout(
            title=dict(font=dict(size=28), # Taille
                       x=0.5, # Position
                       xanchor='center',), # Centrage
            margin=dict(l=60, # marge gauche
                        r=60, # marge droite
                        t=50, # marge haut
                        b=50, # marge bas
                        ),
            )

        return ('The input value was "{}" and the button has been \
                clicked {} times'.format(val_selected, num_clicks), # Zone texte
                fig # Graphique
                )

if __name__ == '__main__':
    app.run_server(debug=True)
