"""
Lien : https://www.youtube.com/watch?v=dgV3GGFMcTc
Cours : DataTable (Dropdown) - Dash Plotly Python

Dans ce programme, on travaille toujours sur le widget dashtable, mais cette fois-ci
on ajoute en plus du graphique, du widget menu déroulant 'drop down'

Les données visualisées représentent le nombre de personnes ayant eu le COVID, ainsi
que le nombre de personnes tuées par le COVID par pays, sur une période déterminée.

Date : 24-08-23
"""

import pandas as pd   
import plotly.express as px
from dash import Dash, dash_table, html, dcc, Input, Output

# Instanciation de la librairie
app = Dash(__name__)

#---------------------------------------------------------------
# Récupération du fichier Excel converti en DF pandas
df = pd.read_excel("data/COVID-19-geographic-disbtribution-worldwide-2020-03-29.xlsx")

# Regroupement des données sous le champ countriesAndTerritories : 
# nombre de morts et de cas
dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()
print (dff[:5])

#---------------------------------------------------------------
# Configuration de la page @
app.layout = html.Div([
    html.Div([
        
        # Datatable
        dash_table.DataTable(
            id='datatable_id', # pour l'ID callback
            data=dff.to_dict('records'), # Récupération des données de la DF
            columns=[ # Options pour chaque colonne (compréhension de liste)
                {"name": i, "id": i, 
                 "deletable": False, # Supprimer la colonne
                 "selectable": False} # Sélectionner la conne
                for i in dff.columns],
            editable=False, # Pas modifiable
            filter_action="native", # Filtre activée
            sort_action="native", # Trie activée
            sort_mode="multi", # Multi trie activée
            row_selectable="multi", # Multi sélection des lignes activée
            row_deletable=False, # Les lignes ne peuvent pas être supprimés
            selected_rows=[], # pour la fonctionnalité callback (property)
            page_action="native", # plusieurs pages admis
            page_current= 0, # page par défaut à afficher : première page
            page_size= 6, # nombre de lignes par pages
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[ # Format des colonnes
                {'if': {'column_id': 'countriesAndTerritories'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'deaths'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'), # 1ère ligne

    # Section
    html.Div([
        
        # Sous-section
        html.Div([
            
            # 1er menu déroulant déroulant
            dcc.Dropdown(
                id='linedropdown', # pour l'ID callback
                options=[ # Données du menu déroulant
                         {'label': 'Deaths', # Donnée affichée
                          'value': 'deaths'}, # pour la fonctionnalité callback
                         {'label': 'Cases', # Donnée affichée
                          'value': 'cases'}], # pour la fonctionnalité callback
                value='deaths', # Valeur par défaut à afficher au menu
                multi=False, # pas de possibilité de sélectionner plusieurs valeurs
                clearable=False # pas de possibilité de supprimer les valeurs
            ),
        ],className='six columns'), # largeur de la sous-section

        # Sous-section
        html.Div([
            
            # 2ème menu déroulant
            dcc.Dropdown(
                id='piedropdown', # pour l'ID callback
                options=[ # Données du menu déroulant
                     {'label': 'Deaths', # Donnée affichée
                      'value': 'deaths'}, # pour la fonctionnalité callback
                     {'label': 'Cases', # Donnée affichée
                      'value': 'cases'}], # pour la fonctionnalité callback
                value='cases', # Valeur par défaut à afficher au menu
                multi=False, # pas de possibilité de sélectionner plusieurs valeurs
                clearable=False # pas de possibilité de supprimer les valeurs
        ),
        ],className='six columns'), # largeur de la sous-section

    ],className='row'), # 2ème ligne

    # Section
    html.Div([
        
        # Sous-section
        html.Div([
            
            # 1er graphique vide
            dcc.Graph(id='linechart'),
            ],className='six columns'), # largeur de la sous-section

        # Sous-section
        html.Div([
            
            # 2ème graphique vide
            dcc.Graph(id='piechart'),
        ],className='six columns'), # largeur de la sous-section

    ],className='row'), # 3ème ligne

])

#------------------------------------------------------------------
# MAJ des deux graphiques selon les lignes sélectionnés dans la datatable et
# les valeurs sélectionnées dans les 2 menus déroulants
@app.callback(
    [Output( # Sortie concernant le 2ème graphique (camembert)
        # ID : 2ème graphique
        component_id='piechart', 
        # Fonctionnalité : affichage du graphique
        component_property='figure'),
     
     Output( # Sortie concernant le 1er graphique (histogramme)
         # ID : 1er graphique
         component_id='linechart', 
         # Fonctionnalité : affichage du graphique
         component_property='figure')],
    
    
    [Input( # Entrée concernant la datatable
        # ID : datatable
        component_id='datatable_id', 
        # Fonctionnalité : ligne sélectionnée
        component_property='selected_rows'),
     
     Input( # Entrée pour le 2ème menu déroulant
         # ID : 2ème menu déroulant
         component_id='piedropdown', 
         # Fonctionnalité : valeur du menu déroulant
         component_property='value'),
     
     Input( # Entrée pour le 1er menu déroulant
         # ID : 1er menu déroulant
         component_id='linedropdown', 
         # Fonctionnalité : valeur du menu déroulant
         component_property='value')]
)
def update_data(chosen_rows, # entrée 1 : ligne(s) sélectionnée(s) de la datatable
                piedropval, # entrée 2 : valeur du 2ème menu déroulant
                linedropval # entrée 3 : valeur du 1er menu déroulant
                ): 
    
    # Si ma liste est vide (aucune ligne n'est sélectionnée dans ma datatable)
    if len(chosen_rows)==0:
        print(chosen_rows)
        # Filtre de la DF selon les pays suivants : Chine, Iran, Espagne et Italie
        df_filterd = dff[dff['countriesAndTerritories'].isin(
            ['China','Iran','Spain','Italy'])]
    # Sinon si ma liste comporte des n° de composants 
    # (lignes sélectionnées dans ma datatable)
    else: 
        print(chosen_rows)
        # Filtre de la DF selon les pays rattachés aux composants de la liste
        df_filterd = dff[dff.index.isin(chosen_rows)]

    # Graphique en camembert
    pie_chart=px.pie(
            data_frame=df_filterd, # données filtrées de la DF
            names='countriesAndTerritories',
            values=piedropval, # valeur sélectionnée du 2ème menu déroulant
            hole=.3, # largeur du trou central du graphique
            labels={'countriesAndTerritories':'Countries'}
            )

    # Extraction des pays filtrés dans la DF en une liste
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    
    # Récupération de la DF avant le regroupage par pays, afin d'avoir le champ
    # sur les dates, et à cette DF, on effectue un recoupement avec la DF filtrée
    # ci-avant
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    # Histogramme
    line_chart = px.line(
            data_frame=df_line, # données de la DF filtrée
            x='dateRep',
            y=linedropval, # valeur sélectionnée du 1er menu déroulant
            color='countriesAndTerritories', # couleur par pays
            labels={ # Changement des titres
                'countriesAndTerritories':'Countries', 
                'dateRep':'date'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart, line_chart)

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
