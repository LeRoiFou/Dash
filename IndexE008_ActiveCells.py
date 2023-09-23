"""
Lien : https://www.youtube.com/watch?v=-KLtU_t5bXs&list=PLh3I780jNsiSC7QJMQ46tHDYYnfhGEflf&index=8
Cours : DataTable Reactive Cells - Dash Plotly Python

Dans ce cours, on travaille sur les propriétés de la fonctionnalité active_cell
de la datatable, mettant à jour les données à afficher sur le graphique

Documentation comprenant entre autres les propriétés de la fonctionnalité 
active_cell :
https://dash.plotly.com/datatable/reference

Date : 23-09-23
"""

from dash import Dash, dcc, html, Input, Output, dash_table, no_update
import plotly.express as px

# TRAITEMENTS EN DS ------------------------------------------------------------

# Récupération de données dans la librairie plotly converties en DF
df = px.data.gapminder() 

# Ajout d'un champ pour récupérer le n° d'index de chaque ligne de la DF
# Ce champ est indispensable pour la fonctionnalité active_cell de la datatable
# qui se réfère indirectement sur le n° d'index de la DF
df["id"] = df.index

# Filtre sur une année (pour la datatable uniquement)
dff = df[df.year == 2007]

# COMPOSANTS DE LA PAGE @ ----------------------------------------------------

# Champs à afficher pour la datatable
columns = ["country", "continent", "lifeExp", "pop", "gdpPercap"]

# Couleurs pour le graphique
color = {
    "lifeExp": "#636EFA", # Couleur de la ligne pour 'lifeExp'
    "pop": "#EF553B", # Couleur de la ligne pour 'pop'
    "gdpPercap": "#00CC96" # Couleur de la ligne pour 'gdpPercap'
    }

# Instanciation de la cellule sélectionnée par défaut
initial_active_cell = {
    "row": 0,  # 1ère ligne
    "column": 0, # 1ère colonne
    "column_id": "country", # Nom du champ concerné
    "row_id": 0 # N° id concerné
    }

# FRONT END -------------------------------------------------------------------

# Instanciation de la librairie DASH
app = Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Configuration de la page @
app.layout = html.Div(
    [
        html.Div(
            [   
                # Titre
                html.H3("2007 Gap Minder", style={"textAlign":"center"}),
                
                # Datatable
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in columns],
                    data=dff.to_dict("records"),
                    sort_action="native", # pagination active
                    page_size=10, # Nombre de lignes max par page
                    # Données récupérées de la cellule sélectionnée
                    active_cell=initial_active_cell,
                ),
            ],
            style={"margin": 50},
            className="five columns"
        ),
        
        # Zone vide pour le lgraphique
        html.Div(id="output-graph", 
                 className="six columns"),
    ],
    className="row"
)


# FRONT END & BACK END ----------------------------------------------------

#
@app.callback(
    Output("output-graph", "children"), # Sortie : graphique
    Input("table", "active_cell"), # Entrée : datatable
)
def cell_clicked(active_cell):
    
    # Affichage dans le terminal les données de la cellule sélectionnée ---------
    
    print("-------------- Données de la cellule sélectionnée --------------")
    
    # N° du composant de la ligne sélectionnée
    row = active_cell['row']
    print(f"row: {row}")
    
    # N° du composant de la colonne sélectionnée
    column = active_cell['column']
    print(f"column: {column}")
    
    # Nom de la colonne sélectionnée dans la datatable
    column_index = active_cell["column_id"]
    print(f"column id: {column_index}")
    
    # N° d'index selon la ligne sélectionnée dans la datatable
    row_index = active_cell["row_id"]
    print(f"row id: {row_index}")
    
    print("---------------------------------------------------------------")

    # Ciblage de la cellule avec l'instruction 'at' opérée sur la DF :
    # en fonction du n° d'index instanciée ci-avant de la ligne sélectionnée dans
    # la DF et du champ 'country', récupération du nom du pays
    country = df.at[row_index, "country"] # = DF.at[n° index ligne, nom_du_champ]
    print(country)
    
    # Traitements opérés ---------------------------------------------------------
    
    # Si aucune cellule n'est sélectionnée dans la datatable
    if active_cell is None:
        return no_update # Ne pas mettre à jour le graphique

    # Si la colonne sélectionnée est 'pop' ou 'gdpPercap' dans la datatable, alors
    # récupération des valeurs selon l'une de ces colonnes sélectionnées, à défaut,
    # quelque soit la colonne sélectionnée, récupération des valeurs de la colonne
    # lifeExp. L'instruction column_index a été instanciée ci-avant
    y = column_index if column_index in ["pop", "gdpPercap"] else "lifeExp"

    # MAJ du graphique : diagramme en ligne
    fig = px.line(
        df[df["country"] == country], # DF filtrée selon le pays sélectionné
        x="year", # La datatable est filtrée sur 2017, mais pas le graphique !
        y=y, # Données assignées ci-avant
        title=" ".join([country, y]) # Titre
    )
    
    # Mise en forme du graphique
    fig.update_layout(title={"font_size": 20},  
                      title_x=0.5, 
                      margin=dict(t=190, r=15, l=5, b=5))
    
    # Mise à jour de la couleur de la ligne du graphique
    fig.update_traces(line=dict(color=color[y]))

    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)
