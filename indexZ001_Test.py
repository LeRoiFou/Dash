from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input, Output

import polars as pl
import plotly.express as px

# ------------------------------------------------------------------------------
# Récupération de la DF
df_pl = pl.scan_csv('C:/Users/LRCOM/Documents/Laurent/DSCF/Audit/data/539261404FEC20191231.csv')

# Récupération des lignes de comptes de charges
df_f1 = df_pl.filter(pl.col('Compte').str.contains('^6'))

# Regroupage par date
df_g1 = (df_f1.groupby('EcritureDate_time').agg(pl.col('Solde créditeur').sum())
         .sort(by='EcritureDate_time'))

# Changement d'intitule
df_r1 = df_g1.rename({'EcritureDate_time':'Date'})

# Nouvelle colonne
df_w1 = df_r1.with_columns((-pl.col('Solde créditeur')).cast(
    pl.Int32).alias('Montant'))

# Champs à afficher
df_w1 = df_w1.collect()[['Date', 'Montant']]

# Conversion de la df en pandas
df1_pd = df_w1.to_pandas()

# Graphique adapté à cette DF (diagramme en barre)
fig = px.bar(df1_pd, x='Date', y='Montant')

# ------------------------------------------------------------------------------

# Style de la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Titre principal
    html.H1(children="Analyse des charges", 
            style={'textAlign':'Center', 'color':'#241ed8'}),
    
    # Ligne séparatrice
    html.Hr(),
    
    # 1er bloc de section
    html.Div(children=[
        
        # Titre
        html.H3(children="Répartition des charges sur l'exercice",
                style={'textAlign':'Center', 'color':'#4741ea'}),
        
        # DF sur les charges constatées sur l'exercice
        html.Div(children=[  
            # DF
            dash_table.DataTable(
                data=df1_pd.to_dict('records'), 
                columns=[{"name": i, "id": i} for i in df1_pd.columns],
                cell_selectable=True,
                filter_action="native",
                sort_action='native',
                page_action='native',
                page_size=10,
                page_current=0,
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': '#d9e3fc',
                    'color': 'black',
                    'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                    'backgroundColor': '#d9e3fc',}],
                export_format='xlsx')
            
            ], style={'display':'inline-block',
                        'width':'700px'}),
        
        # Graphique sur les charges constatées sur l'exercice
        html.Div(children=[
            
            # Graphique diagramme en barre
            dcc.Graph(figure=fig)
            
            ], style={'display':'inline-block',
                    'width':'800px'}),
        ]),
    ])
    
    


if __name__ == '__main__':
    
    app.run_server(debug=True)
