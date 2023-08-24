"""
Lien : https://www.youtube.com/watch?v=S8ZcErBpfYE
Cours : How to Format the Dash DataTable

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
                # Si le champ Elapsed Days a une valeur supérieure à 40 et
                # inférieure à 60, alors appliqué la couleur de fond 'hotpink'
                # et la couleur blanche du texte
                {
                    'if': {
                        'filter_query': '{Elapsed Days} > 40 && {Elapsed Days} < 60',
                        'column_id': 'Elapsed Days'
                    },
                    'backgroundColor': 'hotpink',
                    'color': 'white'
                },
                # Si le champ Country est filtré sur le pays Canada, alors appliquer
                # la couleur de fond '#FFFF00'
                {
                    'if': {
                        'filter_query': '{Country} = Canada'
                    },
                    'backgroundColor': '#FFFF00',
                },
                # Si le champ 'Part sent date' a une valeur supérieure au champ
                # 'Part received date', alors appliqué la mise en gras du champ
                # 'Part sent date' avec un texte de couleur rouge
                {
                    'if': {
                        'filter_query': '{Part sent date} > {Part received date}',
                        'column_id': 'Part sent date'
                    },
                    'fontWeight': 'bold',
                    'color': 'red'
                },
                # Si une cellule du champ 'Origin supplier' est vide, alors
                # appliquer un fond de couleur gris
                {
                    'if': {
                        'filter_query': '{Origin supplier} is blank',
                        'column_id': 'Origin supplier'
                    },
                    'backgroundColor': 'gray',
                },
                # Si le champ est de type 'text', alignement à gauche
                {
                    'if': {
                        'column_type': 'text'
                        # 'text' | 'any' | 'datetime' | 'numeric'
                    },
                    'textAlign': 'left'
                },
                # Format any cell/row you want ************************
                {
                    'if': {
                        'row_index': 0,
                        'column_id': 'Feedback'
                    },
                    'backgroundColor': 'purple',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                # Format active cells *********************************
                {
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'border': '3px solid rgb(0, 116, 217)'
                },
                {
                    'if': {
                        'column_editable': False  # True | False
                    },
                    'cursor': 'not-allowed'
                },
            ]

            +

            [   # Highlighting bottom three values in a column ********
                {
                    'if': {
                        'filter_query': '{{Machines}} = {}'.format(i),
                        'column_id': 'Machines',
                    },
                    'backgroundColor': '#7FDBFF',
                    'color': 'white'
                }
                for i in df['Machines'].nsmallest(3)
            ]

            +

            # Adding data bars to numerical columns *******************
            data_bars(df, 'Serial number')

        )
    ),

    # Graphique vide de données
    html.Div(dcc.Graph(id='mybar', 
                       figure={}))
])


@app.callback(
    Output(component_id='mybar', component_property='figure'),
    Input(component_id='mydatatable', component_property='derived_virtual_data')
)
def table_to_graph(row_data):
    df_table = df if row_data is None else pd.DataFrame(row_data)
    fig = px.bar(df_table, x='Country', y='Machines')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
