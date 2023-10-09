"""
Lien : https://www.youtube.com/watch?v=3KYf_9ZFsYk&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=18
Cours : Dash Image Annotations and Canvas - Plotly

Documentation Image Annotations with Dash :
https://dash.plotly.com/annotations

Documentation Introduction to dash-canvas (paint):
https://dash.plotly.com/canvas

Documentation sur l'insertion de nouveaux boutons dans un composant 
(modeBarButtonsToAdd): 
https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js

- Insertion de boutons supplémentaires dans un composant
- DashCanvas : équivalent à Paint
- Insertion d'images

Date : 09-10-23
"""

from dash import Dash, html, dcc, Output, Input, callback  
import dash_bootstrap_components as dbc   
from dash_canvas import DashCanvas # Canevas (paint)
import dash_daq as daq  # Boîte à couleurs
import plotly.express as px
import pandas as pd                                       
from skimage import data # Insertion d'images

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Late-Stage_Female_Breast_Cancer_Incidence_Rate__cases_per_100_000_females.csv")

# COMPOSANTS FRONT END -------------------------------------------------------

# Bouton d'options supplémentaires ajoutés au composant concerné
btns = [
    "drawline", # ligne droite
    "drawopenpath", # ligne manuelle
    "drawclosedpath", # cercle manuel
    "drawcircle", # cercle
    "drawrect", # rectanble
    "eraseshape", # sélection de la figure géomatrique dessinée
]

# Récupération d'une image
img = data.skin()
fig_img = px.imshow(img).update_layout(
    dragmode="drawclosedpath" # possibilité de dessiner cercles manuels
    )
# more dragmode option -- https://plotly.com/python/reference/layout/#layout-dragmode

# Nuage de points
fig_scatter = px.scatter(
    data_frame=df, 
    x='Year', 
    y='Rate (per 100,000 females)',
    color='Race'
    )

# FRONT END ------------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configuration de la page @
app.layout = dbc.Container([
    
    # Titre principal
    html.H1("Late-Stage Female Breast Cancer", 
            style={'textAlign': 'center'}),
    
    dbc.Row([
        
        dbc.Col([
            
            # Nuage de points
            dcc.Graph(figure=fig_scatter, 
                      config={"modeBarButtonsToAdd": btns}, # ajout boutons sup
                      )
        ], width=8),
        
        dbc.Col([
            
            # Sous-titre
            html.H2('Take Notes:'),
            
            # Canevas (paint)
            DashCanvas(id='my-canvas', # pour le callback
                       tool='pencil', # outil par défaut pour dessiner
                       lineWidth=10, # largeur du feutre pour dessiner
            )
        ], width=4, className='mt-5')
    ]),
    
    dbc.Row([
        
        dbc.Col([
            
            # Graphique : insertion d'une photo
            dcc.Graph(
                figure=fig_img, 
                config={"modeBarButtonsToAdd": btns},  # ajout boutons sup
                )
        ], width=6),
        
        dbc.Col([
            
            # Boite à couleurs
            daq.ColorPicker(
                id='color-picker', # pour le callback
                label='Brush color', # titre
                value=dict(hex='#119DFF'), # couleur par défaut
            )], width=4, className='mt-5')
    ])
], fluid=True)

# INTERACTION DES COMPOSANTS ---------------------------------------------

# Selon la couleur choisie dans la boîte à couleur, celle-ci sera appliquée pour
# le composant canevas (paint)
@callback(
    Output(component_id='my-canvas', # Sortie : canevas (paint)
           component_property='lineColor'),
    Input(component_id='color-picker', # Entrée : boîte à couleurs
          component_property='value')
)
def update_canvas_linecolor(value):
    if isinstance(value, dict):
        return value['hex']
    else:
        return value


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
