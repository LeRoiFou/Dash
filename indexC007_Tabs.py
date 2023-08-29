"""
Lien : https://www.youtube.com/watch?v=g3VQAVz_0qo
Cours : Create Multiple Tabs in Plotly Dash to Make a Finance Dashboard | #213 (Plotly Dash #7)

Dans ce cours, on utilise les onglets, la problématique et que chaque composant
des onglets doivent être argumentés dans une fonction callback, ce qui est assez
lourd pour suivre le cheminement d'un script...

Date : 29-08-23
"""

from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)

app.layout = html.Div(
    children=[
    
    # Mise en place des onglets
    dcc.Tabs(id='tabs', 
             value='tab-2', # Onglet à afficher par défaut
             children=[ # Onglets à afficher
                 dcc.Tab(label='Onglet n° 1', value='tab-1'),
                 dcc.Tab(label='Onglet n° 2', value='tab-2')
    ]),
    
    html.Div(id='tab-content')
    ])

@app.callback(
    Output(
        component_id='tab-content',
        component_property='children'),
    Input(
        component_id='tabs',
        component_property='value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1("Titre pour l'onglet n° 1")])
    else:
        return html.Div([
            html.H1("Titre pour l'onglet n° 2")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
