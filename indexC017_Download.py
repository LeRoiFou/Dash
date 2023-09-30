"""
Lien : https://www.youtube.com/watch?v=LYdLiXumdxs&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=10
Cours : Download component - Plotly Dash

Documentation sur dcc.Download :
https://dash.plotly.com/dash-core-components/download

Icônes pour le bouton de chargement des données :
https://fontawesome.bootstrapcheatsheets.com/

Dans ce cours on apprend à télécharger les données à partir du composant download,
et également la mise en forme du bouton de téléchargement des données en insérant
un icône à partir de l'URL ci-avant

Date : 30-09-23
"""

from dash import Dash, html, dcc, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Assignation de la récupération du fichier .css à partir du site pour charger
# les icônes pour la page @ : 
# https://fontawesome.bootstrapcheatsheets.com/
FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

# Mise en forme de la page @
external_stylesheets = [
    dbc.themes.BOOTSTRAP, 
    FONT_AWESOME # Pour insérer les icônes sur la page @
    ]

# Instanciation de la sous-librairie Dash
app = Dash(__name__, 
           external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = dbc.Container(
    [   
        # Datatable chargées à partir de la DF récupérée ci-avant
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        ),

        # Bouton d'exécution
        dbc.Button(id='btn',
            children=[
                # Copie sur le site des icônes, de l'image intitué ".fa-download",
                # le script HTML : <i class="fa fa-download"></i>
                html.I(className="fa fa-download mr-1"), 
                " Download" # Texte du bouton d'exécution
                ],
            color="info", # Couleur cyan
            className="mt-1" # Espacement entre le bouton et la datatable
        ),

        # Téléchargement des données (n'apparaît pas sur la page @)
        dcc.Download(id="download-component"),
    ],
    className='m-4'
)

# Interaction des composants : téléchargement des données dès bouton exécuté
@callback(
    Output("download-component", "data"), # Sortie : téléchargement des données
    Input("btn", "n_clicks"), # Entrée : bouton d'exécution
    
    # False : téléchargement auto du fichier car la fonctionnalité du bouton 
    # d'exécution n_clicks = 0 par défaut, il considère donc que même sans appuyer
    # sur le bouton, il faut télécharger le fichier
    prevent_initial_call=True, 
)
def func(n_clicks):
    
    # Téléchargement d'un fichier .txt avec un contenu de texte
    # return dict(
    #     content="Always remember, we're better together.", # Texte dans le fichier
    #     filename="hello.txt" # Nom et format du fichier téléchargé
    #     )
    
    # Téléchargement des données de la DF au format .csv
    # return dcc.send_data_frame(
    #     df.to_csv, # Conversion de la DF pandas en fichier .csv
    #     "mydf_csv.csv" # Nom et format du fichier téléchargé
    #     )
    
    # Téléchargement des données de la DF au format .xlsx
    return dcc.send_data_frame(
        df.to_excel, # Conversion de la DF pandas en fichier excel
        "mydf_excel.xlsx", # Nom et format du fichier téléchargé
        sheet_name="Sheet_name_1" # Nom de l'onglet du fichier excel
        )


if __name__ == "__main__":
    app.run_server(debug=True)
