"""
Lien : https://www.youtube.com/watch?v=VZ6IdRMc0RI&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=8
Cours : Input Box - Python Dash Plotly

Documentation sur le composant dcc.Input :
https://dash.plotly.com/dash-core-components/input

Date : 27-09-23
"""

from dash import Dash, dcc, html, Input, Output
import datetime

# FRONT END ---------------------------------------------------------------------

# Instanciation de la librairie
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
    
    html.Div([
        
        # Zone de saisie
        dcc.Input(
            id='my_txt_input',
            type='text',
            debounce=True, # True -> appuyez sur Entrée pour MAJ des valeurs
            pattern=r"^[A-Za-z].*", # Regex : le 1er caractère est une lettre
            spellCheck=True, # True : correcteur d'orthographe
            inputMode='latin', # Type de donnée saisie
            name='text', # pour le callback
            list='browser', # Récup des données de la liste ci-après par son ID
            n_submit=0,
            n_submit_timestamp=-1,
            autoFocus=True,  
            n_blur=0,  
            n_blur_timestamp=-1, 
            # selectionDirection='',
            # selectionStart='', 
            # selectionEnd='', 
        ),
    ]),

    # Liste (pour la zone de saisie ci-avant)
    html.Datalist(id='browser', children=[
        html.Option(value="blue"),
        html.Option(value="yellow"),
        html.Option(value="green")
    ]),

    # Retours chariots
    html.Br(),
    html.Br(),

    # Zone de texte vide
    html.Div(id='div_output'),

    # Saisie
    html.P(['------------------------']),

    # Saisie
    html.P(['Enter clicked:']),
    
    # Zone de texte vide
    html.Div(id='div_enter_clicked'),

    # Saisie
    html.P(['Enter clicked timestamp:']),
    
    # Zone de texte vide
    html.Div(id='div_sub_tmstp'),

    html.P(['------------------------']),

    # Saisie
    html.P(['Input lost focus:']),
    
    # Zone de texte vide
    html.Div(id='div_lost_foc'),

    # Saisie
    html.P(['Lost focus timestamp:']),
    
    # Zone de texte vide
    html.Div(id='div_lst_foc_tmstp'),

])

# INTERACTIONS ENTRE COMPOSANTS ------------------------------------------------

# ???
@app.callback(
    [Output(component_id='div_output', component_property='children'),
     Output(component_id='div_enter_clicked', component_property='children'),
     Output(component_id='div_sub_tmstp', component_property='children'),
     Output(component_id='div_lost_foc', component_property='children'),
     Output(component_id='div_lst_foc_tmstp', component_property='children')],
    [Input(component_id='my_txt_input', component_property='value'),
     Input(component_id='my_txt_input', component_property='n_submit'),
     Input(component_id='my_txt_input', component_property='n_submit_timestamp'),
     Input(component_id='my_txt_input', component_property='n_blur'),
     Input(component_id='my_txt_input', component_property='n_blur_timestamp')]
)
def update_graph(txt_inserted, num_submit, sub_tmstp, lost_foc, lst_foc_tmstp):
    if sub_tmstp == -1:
        submited_dt = sub_tmstp
    else:
        submited_dt = datetime.datetime.fromtimestamp(int(sub_tmstp) / 1000)  # using the local timezone
        submited_dt = submited_dt.strftime("%Y-%m-%d %H:%M:%S")

    if lst_foc_tmstp == -1:
        lost_foc_dt = lst_foc_tmstp
    else:
        lost_foc_dt = datetime.datetime.fromtimestamp(int(lst_foc_tmstp) / 1000)  # using the local timezone
        lost_foc_dt = lost_foc_dt.strftime("%Y-%m-%d %H:%M:%S")

    return txt_inserted, num_submit, submited_dt, lost_foc, lost_foc_dt


# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
