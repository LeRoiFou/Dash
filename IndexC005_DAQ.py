"""
Cours : [Introduction to Dash DAQ for manufacturing dashboards](https://youtu.be/t3cLkzJAUgo)

Documentation sur DAS DAQ
[Dash DAQ](https://dash.plotly.com/dash-daq)

2ème application

Date : 21-08-23
"""

from dash import Dash, html, Input, Output
import dash_daq as daq

# *************************************************************************
# Style de la page @
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Instanciation de la librairie
app = Dash(__name__, external_stylesheets=external_stylesheets)

# *************************************************************************
# Configuration de la page @
app.layout = html.Div(
    [
        # Section
        html.Div(
            [
                # Titre
                html.H1("Room Temperature"),
                
                # Section
                html.Div(
                    
                    # Bouton du four
                    daq.Knob(
                        id="my-knob",
                        label="Set Temperature",
                        min=30,
                        max=100,
                        value=40,
                        scale={"start": 40, "labelInterval": 10, "interval": 10},
                        color={
                            "gradient": True,
                            "ranges": {"blue": [30, 75], 
                                       "red": [75, 100]}}),
                    className="two columns"),
                
                # Section
                html.Div(
                    
                    # Thermomètre
                    daq.Thermometer(
                        id="my-thermometer", 
                        min=30, 
                        max=99, 
                        value=40),
                    className="three columns")
                
            ], className="row"),
        
        # Section
        html.Div(
            [
                # Section
                html.Div(
                    
                    # Affichage LED
                    daq.LEDDisplay(
                        id="my-leddisplay", 
                        value="40", 
                        color="#39FF14"),
                    className="four columns"),
                
                # Section
                html.Div(
                    
                    # Sélecteur de couleurs
                    daq.ColorPicker(
                        id="my-colorpicker",
                        label="Choose display color",
                        value={"hex": "#39FF14"}),
                    className="three columns"),
            
            ],className="row",
        )])


# *************************************************************************
# La valeur du bouton du four va avoir une incidence sur l'affichage de valeur
# du thermomètre et de la valeur affichée sur le LED
# Et la couleur sélectionnée au sélecteur de couleur va avoir une incidence sur
# la couleur d'affichage du LED
@app.callback(
    Output( # Sortie
        "my-thermometer", # Thermomètre
        "value"), # Affichage de la valeur
    Output( # Sortie
        "my-leddisplay", # Affichage LED
        "value"), # Valeur affichée
    Output( # Sortie
        "my-leddisplay", # Affichage LED
        "color"), # Couleur d'affichage
    Input( # Entrée
        "my-knob", # Bouton du four
        "value"), # Valeur du bouton du four sélectionnée
    Input( # Entrée
        "my-colorpicker", # Sélecteur de couleur
        "value"), # Code couleur sélectionnée
)
def update(knob_value, color_chosen): # 2 arguments = 2 entrées
    return ( # 3 variables = 3 sorties
        knob_value, # modification de la valeur du thermomètre
        knob_value, # modification de la valeur affichée au LED
        color_chosen["hex"]) # modification de la couleur d'affichage du LED

if __name__ == "__main__":
    app.run_server(port=3040, debug=True)
