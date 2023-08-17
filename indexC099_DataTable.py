"""
Lien : https://www.youtube.com/watch?v=USTqY4gH_VM&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=2
Cours : Introduction to Dash DataTable - Growing a Spreadsheet into an Application

Ce n'est pas parce qu'il y  a 8 entrées que forcement il y aura 8 widgets : les 
multiples entrées d'un callback peuvent porter sur un seul widget

Date : 17-08-2023
"""

from dash import Dash    
from dash import dash_table
from dash import html
from dash import dcc
from dash import Input, Output

import pandas as pd
import plotly.express as px

#---------------------------------------------------------------------------------
# Récupération du fichier .CSV en DF pandas
df = pd.read_csv('data/internet_cleaned.csv')

# Filtre sur une année du champ 'year'
df = df[df['year'] == 2019]

# Nouvelle colonne en tant qu'ID de la DF
df['id'] = df['iso_alpha3']
df.set_index('id', inplace=True, drop=False)

#---------------------------------------------------------------------------------
# Instanciation de la librairie
app = Dash(__name__)

# Configuration de la page web
app.layout = html.Div(children=[
    
    # DF
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name":i, "id":i, "deletable":True, "selectable":True,
             "hideable":True}
            if i=='iso_alpha3' or i=='year' or i=='id'
            else {'name':i, 'id':i, 'deletable':True, 'selectable':True}
            for i in df.columns],
        data=df.to_dict('records'), # contenu de la DF
        editable=True, # cellule de la DF modifiable
        filter_action='native', # ou 'none' -> filtre sur le champ
        sort_action='native', # trie
        sort_mode='single', # ou 'multi' -> trie du 1er champ de la table
        column_selectable='multi', # possibilité de sélectionner plusieurs champs
        row_selectable='multi', # possibilité de sélectionner plusieurs lignes
        row_deletable=True, # possibilité de supprimer des lignes
        selected_columns=[],
        selected_rows=[],
        page_action='native',
        page_current=0, # Page par défaut à afficher
        page_size=6, # Nombre de lignes par page
        style_cell= # Taille des cellules adaptées si la fenêtre est diminuée
        {'minWidth':95, 'maxWidth':95, 'width':95},
        style_cell_conditional=[{ # Alignement si certains champs sont centrés (c)
            'if':{'column_id':c}, 'textAlign':'left'}
            for c in ['country', 'iso_alpha3']],
        style_data={ # Retour à la ligne des données d'une cellule
            'whiteSpace':'normal',
            'height':'auto'}),
    
    # Sauts de ligne
    html.Br(),
    html.Br(),
    
    # Textes vides
    html.Div(children='', id='bar-container'),
    html.Div(children='', id='choromap-container')
])

#---------------------------------------------------------------------------------
# Create bar chart
@app.callback(
    # Sortie : le premier texte vide
    Output(component_id='bar-container', component_property='children'),
    # Entrées : uniquement la DF
    [Input(component_id='datatable-interactivity', 
           # Toutes les données de la DF :
           component_property="derived_virtual_data"), 
     Input(component_id='datatable-interactivity', 
           # N° d'indice des lignes sélectionnées
           component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', 
           # Nom de l'ID des lignes sélectionnées (['AUT'] ou ['BEL'] ou...)
           component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', 
           # N° d'indice des lignes sélectionnées
           component_property='selected_rows'),
     Input(component_id='datatable-interactivity', 
           # Liste des n° de composants des lignes non filtrées
           component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', 
           # Liste des noms d'ID non filtréS
           component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', 
           # Données (N° de ligne, n° de colonne...) de la cellule sélectionnée
           component_property='active_cell'),
     Input(component_id='datatable-interactivity', 
           # Données (N° de ligne, n° de colonne...) de la cellule sélectionnée
           component_property='selected_cells')])
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    print('***************************************************************************')
    print(f'Data across all pages pre or post filtering: {all_rows_data}')
    print('---------------------------------------------')
    print(f"Indices of selected rows if part of table after filtering: {slctd_row_indices}")
    print(f"Names of selected rows if part of table after filtering: {slct_rows_names}")
    print(f"Indices of selected rows regardless of filtering results: {slctd_rows}")
    print('---------------------------------------------')
    print(f"Indices of all rows pre or post filtering: {order_of_rows_indices}")
    print(f"Names of all rows pre or post filtering: {order_of_rows_names}")
    print(f"---------------------------------------------")
    print(f"Complete data of active cell: {actv_cell}")
    print(f"Complete data of all selected cells: {slctd_cell}")

    dff = pd.DataFrame(all_rows_data)

    # used to highlight selected countries on bar chart
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    # Si ces deux champs sont présents dans la DF
    if "country" in dff and "did online course" in dff:
        return [
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(
                    data_frame=dff,
                    x="country",
                    y='did online course',
                    labels={"did online course": "% of Pop took online course"}
                    ).update_layout(
                        showlegend=False, 
                        xaxis={'categoryorder': 'total ascending'})
                    .update_traces(
                        marker_color=colors, 
                        hovertemplate="<b>%{y}%</b><extra></extra>"))
        ]


#---------------------------------------------------------------------------------
# Create choropleth map
@app.callback(
    Output( # Sortie : le deuxième texte vide
        component_id='choromap-container', 
        component_property='children'),
    # Entrées : DF
    [Input(
        component_id='datatable-interactivity', 
        component_property="derived_virtual_data"),
     Input(
         component_id='datatable-interactivity', 
         component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "iso_alpha3" in dff and "internet daily" in dff and "country" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          data_frame=dff,
                          locations="iso_alpha3",
                          scope="europe",
                          color="internet daily",
                          title="% of Pop that Uses Internet Daily",
                          template='plotly_dark',
                          hover_data=['country', 'internet daily'],
                      ).update_layout(
                          showlegend=False, 
                          title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(
                          marker_line_width=borders, 
                          hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                          "%{customdata[1]}" + "%"))
        ]


#---------------------------------------------------------------------------------
# Highlight selected column
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


#---------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
    