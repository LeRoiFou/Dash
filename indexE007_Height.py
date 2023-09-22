"""
Lien : https://www.youtube.com/watch?v=twHtUFR7rtw&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=7
Cours : DataTable Styling & Height -- Dash Plotly

Documentation - hauteur des datatables :
https://dash.plotly.com/datatable/height

Documentation - propriétés des datatables :
https://dash.plotly.com/datatable/reference

Par défaut, chaque ligne, y compris les en-têtes, la hauteur est de 30 pixels

NOTE IMPORTE SUR LES LIGNES À AFFICHER :
Si vous avez plus de 1 000 lignes, votre navigateur sera ralenti. 
C'est pourquoi, pour plus de 1 000 lignes, utilisez la pagination 
comme dans les exemples ci-après ou recourir à la virtualisation avec l'instruction
virtualization=True

Présentation de la pagination de la datatable selon 3 situations.

Date : 22-09-23
"""

from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict

app = Dash(__name__)

#-----------------------------------------------------------------------------
# Assignation d'une DF pandas à partir d'un OrderedDict de la librairie collections
data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", 
                  "2017-01-10", "2018-05-10", "2018-08-15",
                  "2015-01-01", "2015-10-24", "2016-05-10", 
                  "2017-01-10", "2018-05-10", "2018-08-15",
                  "2015-01-01", "2015-10-24", "2016-05-10", 
                  "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", 
                    "Miami", "San Francisco", "London",
                    "Montreal", "Toronto", "New York City", 
                    "Miami", "San Francisco", "London",
                    "Montreal", "Toronto", "New York City", 
                    "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2,
                         1, -20, 3.512, 4, 10423, -441.2,
                         1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60,
                      10, 20, 30, 40, 50, 60,
                      10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15,
                      2, 10924, 3912, -10, 3591.2, 15,
                      2, 10924, 3912, -10, 3591.2, 15]),
    ]
)
df = pd.DataFrame(data)

# Configuration de la page @ avec une uniquement une datatable ---------------------

app.layout = dash_table.DataTable(
    
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    
#-----------------------------------------------------------------------------
# 1ERE SITUATION :
# Absence de pagination - Barre de déroulement verticale
#-----------------------------------------------------------------------------
    page_action='none', # Pas de pagination : barre déroulement verticale présente
    fixed_rows={'headers': True}, # Entête figée
    style_table={
        'height': '300px', # Taille de la datatable
        'overflowY': 'auto', # Adaptation de la page
                 },
    virtualization=True, # évite ralentissement si + de 1 000 lignes

#-----------------------------------------------------------------------------
# 2EME SITUATION :
# Pagination SANS barre de déroulement verticale
#-----------------------------------------------------------------------------
    # page_action='native', # Pagination
    # page_size=10, # Nombre de lignes max par page
    
#-----------------------------------------------------------------------------
# 3EME SITUATION :
# Pagination AVEC barre de déroulement verticale
#-----------------------------------------------------------------------------
    # page_action='native', # Pagination
    # page_size=10, # Nombre de lignes max par page
    # style_table={
    #     'height': '100px', # Taille de la datatable
    #     'overflowY': 'auto', # Adaptation de la page
    #     }


)

if __name__ == '__main__':
    app.run_server(debug=True)
