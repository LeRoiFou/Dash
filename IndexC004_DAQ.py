"""
Cours : [Introduction to Dash DAQ for manufacturing dashboards](https://youtu.be/t3cLkzJAUgo)

Documentation sur DAS DAQ
[Dash DAQ](https://dash.plotly.com/dash-daq)

1ère application

Date : 21-08-23
"""
                      
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.graph_objects as go
from random import randrange

# *************************************************************************
# Style de la page @
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Instanciation de la librairie
app = Dash(__name__, external_stylesheets=external_stylesheets)

# *************************************************************************
# Configuration de la page @
app.layout = html.Div(
    
    id="dark-light-theme",
    children=[
        
        # 1ère ligne
        html.Div(
            [
                # Titre
                html.H1("Water Valve Pressure", style={"textAlign": "center"}),
                
                # Section
                html.Div(
                    
                    # Réservoir
                    daq.Tank(
                        id="my-tank",
                        max=400,
                        value=197,
                        showCurrentValue=True,
                        units="gallons",
                        style={"margin-left": "50px"}),
                    className="three columns"),
                
                # Section 
                html.Div(
                    
                    # Jauge n° 1
                    daq.Gauge(
                        id="my-daq-gauge1", 
                        min=0, 
                        max=10, 
                        value=6, 
                        label="Valve 1"),
                    className="four columns"),
                
                # Section
                html.Div(
                    
                    # Jauge n° 2
                    daq.Gauge(
                        id="my-daq-gauge2", 
                        min=0, 
                        max=10, 
                        value=9, 
                        label="Valve 2"),
                    className="four columns"),
            ], className="row"),
        
        # 2ème ligne
        html.Div(
            
            # Section
            html.Div(
                
                # Interrupteur
                daq.ToggleSwitch(
                    id="my-toggle-switch", 
                    label="Liters | Gallons", 
                    value=True),
                className="three columns"),
            className="row"),
        
        # 3ème ligne
        html.Div(
            
            # Graphique vide
            dcc.Graph(
                id="my-graph", 
                figure={}),
            className="row"),
        
        # MAJ page @ sans actualiser avec F5
        dcc.Interval(
            id="timing", 
            interval=1000, 
            n_intervals=0),
    ])


# *************************************************************************
# MAJ des jauges n° 1 et 2 et du graphique selon les le chiffrage qui 
# se génère au hasard à partir du widget de la MAJ de la page @
@app.callback(
    Output( # Sortie
        "my-daq-gauge1", # Jauge n° 1
        "value"), # Affichage de la valeur
    Output( # Sortie
        "my-daq-gauge2", # Jauge n° 1
        "value"), # Affichage de la valeur
    Output(
        "my-graph", # Graphique
        "figure"), # Affichage du graphique
    Input(
        "timing", # MAJ page @ sans actualiser avec F5
        "n_intervals"), # Nombre d'interval
)
def update_g(n_intervals): # un argument = une entrée = MAJ page @
    
    # Données au hasard
    pressure_1 = randrange(10)  # Application sur la jauge n° 1
    pressure_2 = randrange(10)  # Application sur la jauge n° 1

    # MAJ du graphique
    fig = go.Figure(
        [
            go.Bar(
                x=["valve 1", "valve 2"],
                y=[pressure_1, pressure_2], # Deux diagrammes en barres
            )
        ]
    )
    fig.update_layout(yaxis={"range": [0, 10]})

    return ( # 3 variables = 3 sorties
        pressure_1, # Jauge n° 1 : modification de la valeur
        pressure_2, # jauge n° 2 : modification de la valeur
        fig) # MAJ du graphique


# Selon la position de l'interrupteur, l'unité de mesure change sur le réservoir
@app.callback(
    Output( # Sortie
        "my-tank", # Réservoir
        "units"), # L'unité de mesure à afficher
    Input( # Entrée
        "my-toggle-switch", # Interrupteur
        "value"), # Valeur affichée à l'interrupteur
)
def update_g(toggle): # Un argument = une entrée = interrupteur
    if toggle:
        return "gallons" # Affichage 'gallons' au réservoir
    else:
        return "liters" # Affiche 'liters' au réservoir


if __name__ == "__main__":
    app.run_server(debug=True, port=3030)
    