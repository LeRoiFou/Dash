"""
Lien : https://www.youtube.com/watch?v=bQgpC0_XKfI
Cours : Tooltip - Dash Plotly DataTable

Dans ce cours, on apprend à utiliser les infos-bulles dans une datatable

Documentation :
https://dash.plotly.com/datatable/tooltips
https://dash.plotly.com/datatable/reference

Date : 28-08-23
"""

from dash import Dash, dash_table
import pandas as pd 

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/medical_supplies_tooltip.csv")

# Instanciation de la librairie Dash
app = Dash(__name__)

# Configuration de la page @ comprenant uniquement une datatable
app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),

    # Texte à afficher lorsqu'il a une certaine longueur : ici, le texte n'est
    # affiché qu'après un certain nombre de caractères afin d'éviter d'avoir une
    # colonne trop longue
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis', 
        'maxWidth': 0,
    },

    # Paramétrage des info-bulles
    tooltip_delay=0, # 1_000 # Délai d'affichage
    tooltip_duration=None, # 2_000 # Durée d'affichage
    
    # *********************************************************************
    # # Affichage de la valeur de la cellule
    # tooltip_data=[
    #     {
    #         column: {'value': str(value), 'type': 'markdown'}
    #         for column, value in row.items()
    #     } for row in df.to_dict('records')
    # ],
    
    # *********************************************************************
    # # Affichage de l'en-tête de la colonne
    # tooltip={i:
    #     {
    #         'value': i,
    #         'use_with': 'both'  # both refers to header & data cell
    #     } for i in df.columns
    # },
    
    # *********************************************************************
    # Info-bulles pour les deux en-têtes des colonnes ci-après
    tooltip_header={
        'Part description': 'Part description',
        'Origin supplier': 'Suppliers since 1994',
    },
    
    # *********************************************************************
    # Info-bulles pour les deux colonnes ci-après avec des conditions en 
    # recourant à une compréhension de liste
    tooltip_data=[{
        
        # Pour chaque cellule de la colonne 'Machines A', afficher :
        # 'There are [condition 1 - en gras] [condition 2 - en gras] A machines
        # than B machines' avec :
        # condition 1 : valeur cellule Machines A - valeur cellule Machines B
        # condition 2 : Si valeur Machines A > valeur Machine B -> 'more' sinon
        # mentionner 'fewer'
        'Machines A': {
            'value': 'There are **{} {}** A machines than B machines'.format(
                str(abs(row['Machines A'] - row['Machines B'])),
                'more' if row['Machines A'] > row['Machines B'] else 'fewer'
            ),
            'type': 'markdown'
        },
        
        # Pour chaque cellule de la colonne 'Elapsed Days', afficher une photo après
        # le texte 'The shimpent is ', qui sera :
        # -> soit un réveil si la valeur est >= à 18, à défaut un pingouin
        'Elapsed Days': {
            'value': 'The shipment is {}'.format(
                '![Markdown Logo is here.](https://media.giphy.com/media/1xjX6EOQZnS5ouhU5k/giphy.gif)'
                if row['Elapsed Days'] >=18
                else '![Markdown Logo is here.](https://media.giphy.com/media/7SIdExk63rTPXhbbbt/giphy.gif)'
            ),
            'type': 'markdown'
        }
    } for row in df.to_dict('records')], # Pour chaque cellule du dictionnaire
    
    # *********************************************************************
    # # Info-bulles avec des conditions
    # tooltip_conditional=[
        
    #     # Si on passe devant la cellule avec la valeur 'Canada' de la colonne
    #     # 'Country', alors afficher 'Canada row'
    #     {
    #         'if': {
    #             'filter_query': '{Country} eq "Canada"'
    #         },
    #         'type': 'markdown',
    #         'value': 'Canada row.'
    #     },
        
    #     # Si la valeur est négative de la colonne Elapsed Days, alors afficher
    #     # 'Error on Days lapsed in this row.'
    #     {
    #         'if': {
    #             'filter_query': '{Elapsed Days} < 0'
    #         },
    #         'type': 'markdown',
    #         'value': 'Error on Days lapsed in this row.'
    #     }
    # ],
    # *********************************************************************
    
    # Style pour les info-bulles
    css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: purple; color: yellow;'
    }],

)

if __name__=='__main__':
    app.run_server(debug=True)
