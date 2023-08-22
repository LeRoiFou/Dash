"""
Lien : https://www.youtube.com/watch?v=USTqY4gH_VM&list=PLh3I780jNsiSeC7QJMQ46tHDYYnfhGEflf&index=2
Cours : Introduction to Dash DataTable - Growing a Spreadsheet into an Application

Fonctionnalités de DashTable (component_property) :
https://dash.plotly.com/datatable/reference

Dans ce programme, on dispose de 3 callbacks :
- Interactivité d'un graphique en bar (sortie) selon les données sélectionnés 
dans la DF (entrées)
- Interactivité d'un graphique carte géo (sortie) selon les données sélectionnés
dans la DF (entrées)
- Changement de couleur de la ou des colonne(s) sélectionnée(s) dans la DF

Ce n'est pas parce qu'il y a plusieurs entrées que forcement 
il y aura plusieurs widgets concernés : les multiples entrées d'un callback peuvent
porter sur un seul widget et une entrée / sortie peut concerner également un
seul widget

Date : 17-08-2023
"""

from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

#---------------------------------------------------------------------------------
# Récupération du fichier .CSV en DF pandas
df = pd.read_csv('data/internet_cleaned.csv')

# Filtre sur une année du champ 'year'
df = df[df['year'] == 2019]

# Nouvelle colonne en tant qu'ID de la DF afin de pouvoir effectuer certaines
# fonctionnalités dans le callback (ex : derived_virtual_selected_row_ids)
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
            # Chaque colonne peut être supprimée ou être sélectionnés, mais il
            # est également possible de masquer les colonnes iso_alpha3, year et id
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
        selected_columns=[], # À utiliser lors des callback ci-après
        selected_rows=[], # À utiliser lors des callback ci-après
        page_action='native', # 'none' = DF sur une seule page
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
    
    # zones vides
    html.Div(children='', id='bar-container'), # Graphique en bar
    html.Div(children='', id='choromap-container') # Carte géo graphique
])

#---------------------------------------------------------------------------------
# Interactivité d'un graphique en bar (sortie) selon les données sélectionnés
# dans la DF (entrées)
@app.callback(
    
    # Sortie : la 1ère zone vide (graphique en bar)
    Output(
        # ID de la 1ère zone vide
        component_id='bar-container', 
        # Fonctionnalité : valeur
        component_property='children'),
    
    # Entrées : uniquement la DF
    [Input(
        # ID de la DF
        component_id='datatable-interactivity', 
        # Fonctionnalité : 
        # Toutes les données de la DF (même si filtrée)
        component_property="derived_virtual_data"), 
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité : 
         # N° composant(s) de(s) ligne(s) de(s) case(s) cochée(s)
         component_property='derived_virtual_selected_rows'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité : 
         # Nom id (abbrév du pays) de(s) ligne(s) de(s) case(s) cochée(s)
         component_property='derived_virtual_selected_row_ids'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité : 
         # N° composant(s) de(s) ligne(s) des case(s) cochée(s) même si filtrée(s)
         component_property='selected_rows'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity',
         # Fonctionnalité : 
         # Tous les n° de composant(s) des ligne(s) filtrée(s) ou non
         component_property='derived_virtual_indices'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité :
         # Tous les noms id (abbré du pays) de(s) ligne(s) filtrée(s) ou non
         component_property='derived_virtual_row_ids'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité : 
         # Données de la cellule sélectionnée : 
         # {n° ligne, n° de colonne, Nom colonne, référence colonne id}
         component_property='active_cell'),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité :
         # Données de toutes les cellules sélectionnées
         component_property='selected_cells')
     ])
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    
    # print('*********FONCTIONNALITES (PROPERTY) DE LA DATATABLE*********')  
    
    # print(f'Toutes les données de la DF (même si filtrée) : {all_rows_data}')
    
    # print('---------Fonctionnalités avec le(s) case(s) cochée(s)---------------')
    # print(f"N° composant(s) de(s) ligne(s) de(s) case(s) cochée(s) : {slctd_row_indices}") 
    # print(f"Nom id (abbrév du pays) de(s) ligne(s) de(s) case(s) cochée(s) : {slct_rows_names}")
    # print(f"N° composant(s) de(s) ligne(s) des case(s) cochée(s) même si filtrée(s) : {slctd_rows}")
    
    # print('----------Fonctionnalités avec ligne(s) filtrée(s) ou non------------')
    # print(f"Tous les n° de composant(s) de(s) ligne(s) filtrée(s) ou non : {order_of_rows_indices}")
    # print(f"Tous les noms id (abbré du pays) de(s) ligne(s) filtrée(s) ou non : {order_of_rows_names}")
    
    # print(f"--------------Fonctionnalités avec les cellules-----------------")
    # print(f"Données de la cellule sélectionnée : {actv_cell}")
    # print(f"Données de toutes les cellules sélectionnées : {slctd_cell}")
    
    # print('*********************************************************************')  

    # Nouvelle DF récupérant toutes les données
    dff = pd.DataFrame(all_rows_data)

    # Pour chaque composant de la DF 'dff', la couleur est référencée '#7FDBFF'
    # sauf pour le(s) composant(s) sélectionné(s) avec la fonctionnalité 
    # 'slctd_row_indices' (component_property=derived_virtual_selected_rows), 
    # la couleur est référencée '#0074D9'
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    # Si ces deux champs n'ont pas été supprimés la DF 'dff'
    if "country" in dff and "did online course" in dff:
        # Sortie : graphique à barres
        return [
            dcc.Graph(
                id='bar-chart',
                figure=px.bar( # Style de graphique : en barres
                    data_frame=dff, # Données récupérées de la DF 'dff'
                    x="country", # Axe des abscisses
                    y='did online course', # Axe des ordonnées
                    labels={ # Modification du titre à l'axe y
                        "did online course": "% of Pop took online course"}
                    ).update_layout(
                        showlegend=False, # Pas de légende
                        # Trie par ordre croissant des barres du graphique
                        xaxis={'categoryorder': 'total ascending'})
                    .update_traces(
                        # Fonctionnalité rattachée : derived_virtual_selected_rows
                        marker_color=colors, 
                        # Infobulle de la barre : affichage de la valeur y
                        hovertemplate="<b>%{y}%</b><extra></extra>"
                        ))
        ]

#---------------------------------------------------------------------------------
# Interactivité d'un graphique carte géo (sortie) selon les données sélectionnés
# dans la DF (entrées)
@app.callback(
    
    # Sortie : la 2ème zone vide (graphique carte géo)
    Output( 
        # ID de la 2ème zone vide
        component_id='choromap-container', 
        # Fonctionnalité : valeur
        component_property='children'),
    
    # Entrées : uniquement la DF
    [Input(
        # ID de la DF
        component_id='datatable-interactivity', 
        # Fonctionnalité : 
        # Toutes les données de la DF (même si filtrée)
        component_property="derived_virtual_data"),
     
     Input(
         # ID de la DF
         component_id='datatable-interactivity', 
         # Fonctionnalité : 
         # N° composant(s) de(s) ligne(s) de(s) case(s) cochée(s)
         component_property='derived_virtual_selected_rows')
     ])
def update_map(all_rows_data, slctd_row_indices):
    
    # Nouvelle DF récupérant toutes les données
    dff = pd.DataFrame(all_rows_data)

    # Pour chaque composant de la DF 'dff', la bordure est d'épaisseur 1, 
    # sauf pour le(s) composant(s) sélectionné(s) avec la fonctionnalité 
    # 'slctd_row_indices' (component_property=derived_virtual_selected_rows), 
    # la bordure est d'épaisseur 5
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    # Si ces 3 champs n'ont pas été supprimés de la DF 'dff'
    if "iso_alpha3" in dff and "internet daily" in dff and "country" in dff:
        # Sortie : carte graphique géographique
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700}, # Taille en hauteur de la carte
                      figure=px.choropleth(
                          data_frame=dff, # Données récupérées de la DF 'dff'
                          locations="iso_alpha3", # Pays rattaché
                          scope="europe", # Carte de l'Europe
                          # Couleur du pays selon la valeur du champ 'internet daily'
                          color="internet daily", 
                          title="% of Pop that Uses Internet Daily", # Titre
                          template='plotly_dark', # fond de style de la carte géo
                          # Infobulle de la barre selon les champs ci-après
                          hover_data=['country', 'internet daily'],
                      ).update_layout(
                          showlegend=False, # pas de légende
                          title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(
                          # Fonctionnalité rattachée : derived_virtual_selected_rows
                          marker_line_width=borders, 
                          # Infobulle de la carte : affichage de la 
                          hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                          "%{customdata[1]}" + "%"))
        ]

#---------------------------------------------------------------------------------
# Changement de couleur de la ou des colonne(s) sélectionnée(s) dans la DF
@app.callback(
    
    # Sortie : la DF
    Output(
        # ID de la DF
        component_id='datatable-interactivity', 
        # Fonctionnalité :
        # Styles CSS conditionnels pour les cellules de données. 
        # Ceci peut être utilisé pour appliquer des styles aux cellules de données 
        # par colonne.
        component_property='style_data_conditional'),
    
    # Entrée : la DF
    [Input(
        # ID de la DF
        component_id='datatable-interactivity', 
        # Fonctionnalité : 
        # Récupération du nom de(s) colonne(s) sélectionnée(s)
        component_property='selected_columns')]
)
def update_styles(selected_columns):
    
    # Sortie : DF
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


#---------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
    