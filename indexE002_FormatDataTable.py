"""
Lien : https://www.youtube.com/watch?v=S8ZcErBpfYE
Cours : How to Format the Dash DataTable

Dans ce programme, on intervient notamment dans le front-end layout sur les 
conditions à appliquer dans le widget datatable.

Pour les conditions à appliquer pour le widget datatable, il est exigé de manière
conventionelle de présenter le script de la manière suivante :

style_data_conditionale = (
    [{}, {}] -> conditions classiques
    +
    [] -> conditions avec compréhension de liste
    +
    function -> conditions en appelant une fonction
),

Le callback a uniquement pour fonction d'afficher un diagramme en barres à partir
de la datatable

Date : 24-08-2023
"""

from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px
from indexE002_TableBars import data_bars

#-----------------------------------------------------------------------------------
# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv('data/medical supplies.csv')

# Conversion de champs de type date
df["Part sent date"] = pd.to_datetime(df["Part sent date"]).dt.date
df["Part received date"] = pd.to_datetime(df["Part received date"]).dt.date

# Les jolies étoiles !!! selon la valeur du champ 'Machines'
# Dans une DF, on peut mettre des smileys 😎
df['Prioritize'] = df['Machines'].apply(lambda x:
                                        '⭐⭐⭐' if x > 3_000 else (
                                            '⭐⭐' if x > 1_000 else (
                                                '⭐' if x > 500 else '')))

#-----------------------------------------------------------------------------------
# Instanciation de la librairie Dash
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
    
    # Datatable
    dash_table.DataTable(
        id='mydatatable', # ID de la datatable
        # Données des colonnes et modifiables ou non
        # id : nom du champ récupéré de la DF - back-end
        # name : nom de la colonne à afficher dans le front-end
        columns=[
            {'name': 'S/N', 'id': 'Serial number', 'type': 'numeric', 
             'editable': True},
            {'name': 'Machines', 'id': 'Machines', 'type': 'numeric', 
             'editable': False},
            {'name': 'Country', 'id': 'Country', 'type': 'text', 'editable': True},
            {'name': 'Part sent date', 'id': 'Part sent date', 'type': 'datetime', 
             'editable': True},
            {'name': 'Part received date', 'id': 'Part received date', 
             'type': 'datetime', 'editable': True},
            {'name': 'Elapsed Days', 'id': 'Elapsed Days', 'type': 'numeric', 
             'editable': True},
            {'name': 'Origin supplier', 'id': 'Origin supplier', 'type': 'text', 
             'editable': True},
            {'name': 'Feedback', 'id': 'Feedback', 'type': 'text', 'editable': True},
            {'name': 'Prioritize', 'id': 'Prioritize', 'type': 'text', 
             'editable': False},

        ],
        data=df.to_dict('records'), # Alimentation de la datatable
        style_data_conditional=(
            [   
                # ****************************************************************
                # Condition avec 'filter_query' : filtre opéré sur le layout
                # ****************************************************************
             
                # Si le champ Elapsed Days a une valeur supérieure à 40 et
                # inférieure à 60, alors appliquer la couleur de fond 'hotpink'
                # et la couleur blanche du texte
                {
                    'if': {
                        # Condition avec 'filter_query'
                        'filter_query': '{Elapsed Days} > 40 && {Elapsed Days} < 60',
                        # Colonne désignée
                        'column_id': 'Elapsed Days'
                    },
                    # Incidences
                    'backgroundColor': 'hotpink', 'color': 'white'
                },
                
                # Si la valeur 'Canada' est présente, alors appliquer la couleur de 
                # fond jaune sur la ligne concernée
                {
                    'if': {
                        # Condition avec 'filter_query'
                        'filter_query': '{Country} = Canada'
                        # Pas de colonne désignée, s'applique sur toute la ligne
                    },
                    # Incidences
                    'backgroundColor': '#FFFF00',
                },
                
                # Si le champ 'Part sent date' a une valeur supérieure au champ
                # 'Part received date', alors appliqué la mise en gras du champ
                # 'Part sent date' avec un texte de couleur rouge
                {
                    'if': {
                        # Condition avec 'filter_query'
                        'filter_query': '{Part sent date} > {Part received date}',
                        # Colonne concernée
                        'column_id': 'Part sent date'
                    },
                    # Incidences
                    'fontWeight': 'bold', 'color': 'red'
                },
                
                # Si une cellule du champ 'Origin supplier' est vide, alors
                # appliquer un fond de couleur gris
                {
                    'if': {
                        # Condition avec 'filter_query'
                        'filter_query': '{Origin supplier} is blank',
                        # Colonne concernée
                        'column_id': 'Origin supplier'
                    },
                    # Incidences
                    'backgroundColor': 'gray',
                },
                
                # ****************************************************************
                # Condition avec 'column_type' : sélection des colonnes selon un type
                # ****************************************************************
                
                # Si le champ est de type 'text', alignement à gauche
                {
                    'if': {
                        # Condition avec 'column_type' : 'text' ou 'any' ou 
                        # 'datetime' ou 'numeric'
                        'column_type': 'text'
                        # Pas de colonne désignée, s'applique sur toute la ligne
                    },
                    # Incidences
                    'textAlign': 'left'
                },
                
                # ****************************************************************
                # Condition avec 'row_index' : sélection à partir d'un index d'une
                # ligne
                # ****************************************************************
                
                # Couleur de fond violet, texte de couleur blanc et en gras pour
                # la cellule recoupant la 1ère ligne et le champ 'Feedback'
                {
                    'if': {
                        # Condition avec 'row_index'
                        'row_index': 0,
                        # Colonne désignée
                        'column_id': 'Feedback'
                    },
                    # Incidences
                    'backgroundColor': 'purple', 'color': 'white', 
                    'fontWeight': 'bold'
                },
                
                # ****************************************************************
                # Autres conditions : selon cellule sélectionnée dans la datatable
                # ****************************************************************
                
                # Si la cellule a été sélectionné, alors la bordure de cellule
                # est de couleur rgb(0, 116, 217) avec une épaisseur de 3 px
                {
                    'if': {
                        # Condition avec 'state'
                        'state': 'active'  # 'active' | 'selected'
                        # Pas de colonne désignée, s'applique sur toute la ligne
                    },
                    # Incidences
                    'border': '3px solid rgb(0, 116, 217)'
                },
                
                # Si la colonne n'est pas modifiable, affichage d'un symbole 
                # 'sens interdit' à la flêche de la souris
                {
                    'if': {
                        # Condition avec 'column_editable'
                        'column_editable': False  # True | False
                         # Pas de colonne désignée, s'applique sur toute la ligne
                    },
                    # Incidences
                    'cursor': 'not-allowed'
                },
            ]

            +

            # ****************************************************************
            # Séparation de la condition suivante des conditions précédentes, car
            # cette fois-ci on a recours à une compréhension de liste
            # ****************************************************************
            
            [   # pour les 3 premiers composants ayant la plus petite valeur de
                # la colonne 'Machines', appliquer une couleur bleu ciel aux
                # cellules concernées et mettre le texte de couleur blanche
                {
                    'if': {
                        # Condition : filtre opéré sur le layout
                        # ATTENTION !!! PRÉSENCE D'UNE DOUBLE ACCOLADE
                        'filter_query': f'{{Machines}} = {i}',
                        # Colonne concernée
                        'column_id': 'Machines',
                    },
                    # Incidences
                    'backgroundColor': '#7FDBFF', 'color': 'white'
                }
                # Pour les 3 plus petites valeurs de la colonne 'Machines'
                for i in df['Machines'].nsmallest(3)
            ]

            +
            
            # ****************************************************************
            # Ajout d'une fonction des conditions ci-avant
            # ****************************************************************

            # Ajouter des colonnes en barres horizontales dans la colonne
            # 'S/N' dont la taille dépend de la valeur de la cellule à partir
            # de la fonction du fichier indexE002_TableBars instancié dans ce script
            data_bars(df, 'Serial number')

        )
    ),

    # Graphique vide de données
    html.Div(dcc.Graph(id='mybar', 
                       figure={}))
])

# Diagramme en barres présenté à partir des données de la DF
@app.callback( # Front-end
    Output( # Sortie : diagramme en barres
        component_id='mybar', # ID du diagramme en barres
        component_property='figure'), # Fonctionnalité : MAJ du diagramme
    Input( # Entrée : datatable
        component_id='mydatatable',  # ID de la datatable
        component_property='derived_virtual_data') # Fonctionalité : données de la DF
)
def table_to_graph(row_data): # Back-end : une entrée = les données de la DF
    
    # Selon qu'il ya a desonnées ou non dans la DF
    df_table = df if row_data is None else pd.DataFrame(row_data)
    
    # Insertion des données de la DF dans le graphique avec pour abscisses, les
    # données du champ 'Country' et pour ordonnées, les données du champ 'Machines'
    fig = px.bar(df_table, x='Country', y='Machines')
    
    return fig # un retour = une sortie = le graphique


if __name__ == '__main__':
    app.run_server(debug=True)
