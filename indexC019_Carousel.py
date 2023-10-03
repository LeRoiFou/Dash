"""
Lien : https://www.youtube.com/watch?v=5g3_hSMsLms&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=13
Cours : Dash Bootstrap Carousel Component

Documentation sur le composant dbc.Carousel (images défilées) :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/carousel/

Dans ce cours on utilise le composant carousel qui permet de faire défiler des 
images (on a vu ça avec tkinter, tu te rappelles ?)

Les images à charger, doivent obligatoirement être dans un sous-répertoire au
nom de 'assets'

Date : 03-10-23
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

app.layout = dbc.Container([
    
    # Titre principal
    dbc.Row([
        dbc.Col([
            html.H1("Our Cool Analytics Dashboard", 
                    style={"textAlign":"center"})
        ],width=12)
    ]),
    
    # Images défilées
    dbc.Row([
        dbc.Col([
            dbc.Carousel(
                items=[
                    {"key": "1", # Image n° 1
                     "src": "/assets/Chapulin1.jpg", # Fichier chargé
                     "caption":"My cat captions", # Titre sur l'image
                     "img_style":{"max-height":"500px"} # Taille de l'image
                     },
                    {"key": "2", # Image n° 2
                     "src": "/assets/Chapulin2.jpg", # Fichier chargé
                     "header":"My cat header",  # Titre sur l'image
                     "img_style":{"max-height":"500px"} # Taille de l'image
                     },
                    {"key": "3", # Image n° 3
                     "src": "/assets/Chapulin3.jpg", # Fichier chargé
                     "img_style":{"max-height":"500px"} # Taille de l'image
                     },
                ],
                controls=True, # Défilement manuel des images
                indicators=True, # Indicateur de l'image visualisé en bas d'image
                interval=2_000, # Temps d'intervalle pour passer à l'image suivante
                # className="carousel-fade" # image suivante superposée
            )
        ], width=8)
    ], justify="center"),
    
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
    
