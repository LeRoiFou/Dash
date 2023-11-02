"""
Lien : https://www.youtube.com/watch?v=X3OuhqS8ueM&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=5
Cours : Bootstrap Alerts & Modals - Dash Plotly

Documentation sur les composants HTML :
https://dash.plotly.com/dash-html-components

Thèmes sur Dash :
https://bootswatch.com/default/

Présentation de nouveaux composants avec dbc.Modal() et dbc.Alert() :
-> Affichage d'une nouvelle fenêtre
-> Affichage d'un commentaire
-> Message d'alerte

Date : 02-11-2023
"""

from dash import Dash, dcc, html, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/Berlin_crimes.csv")

# CONFIGURATION DES COMPOSANTS -----------------------------------------------------

# Pour la nouvelle fenêtre
modal = html.Div(
    [   
        # Bouton d'exécution permettant d'ouvrir une nouvelle fenêtre
        dbc.Button("Add comment", # Texte affiché
                   id="open", # pour le callback
                   ),

        # Nouvelle fenêtre
        dbc.Modal([
            
            # En-tête de la nouvelle fenêtre
            dbc.ModalHeader("All About Berlin"),
            
            # Corps principal de la fenêtre
            dbc.ModalBody(
                
                # Regroupage de composants
                dbc.Form(
                    [   
                        # 1er groupe de données
                        dbc.CardGroup(
                            [   
                                # Texte rattaché à la zone de saisie
                                dbc.Label("Name", className="mr-2"),
                                
                                # Zone de saisie
                                dbc.Input(type="text", # Type requis
                                          placeholder="Enter your name", # Affichage
                                          ),
                            ],
                            className="mr-3",
                        ),
                        
                        # 2ème groupe de données
                        dbc.CardGroup(
                            [   
                                # Texte rattaché à la zone de saisie
                                dbc.Label("Email", className="mr-2"),
                                
                                # Zone de saisie
                                dbc.Input(type="email", # Type requis
                                          placeholder="Enter email", # Affichage
                                          ),
                            ],
                            className="mr-3",
                        ),
                        
                        # 3ème groupe de données
                        dbc.CardGroup(
                            [   
                                # Texte rattaché à la zone de saisie
                                dbc.Label("Comment", className="mr-2"),
                                
                                # Zone de saisie
                                dbc.Input(type="text", # Type requis
                                          placeholder="Enter comment", # Affichage
                                          ),
                            ],
                            className="mr-3",
                        ),
                        
                        # Bouton d'exécution
                        dbc.Button("Submit", # Texte affiché
                                   color="primary", # Couleur du bouton
                                   ),
                    ],
                )
            ),
            
            # Pied de page de la fenêtre
            dbc.ModalFooter(
                
                # Bouton d'exécution
                dbc.Button("Close", # Texte affiché
                           id="close",  # Pour le callback
                           className="ml-auto")
            ),

        ],
            id="modal", # pour le callback
            is_open=False, # True : ouverture automatique de la fenêtre
            size="xl", # Taille de la fenêtre : "sm", "lg", "xl"
            backdrop=True, # False : pas de distinct° avec la fenêtre principale
            scrollable=True, # Barre de défilement
            centered=True, # Centré
        ),
    ]
)

# Message d'alerte
alert = dbc.Alert(
    "Please choose Districts from dropdown to avoid further disappointment!", 
    color="danger", # couleur
    dismissable=True, 
    # dismissable=True ou duration=5_000 (par ex) pour clôturer le message 
    # en x milliseconds
    ),  

# Cadre pour les cartes
image_card = dbc.Card(
    [   
        # Carte
        dbc.CardBody(
            [   
                # Titre H4
                html.H4("The Lovely City of Berlin", className="card-title"),
                
                # Image inséré
                dbc.CardImg(src="/assets/berlinwall.jpg", # Fichier chargé
                            title="Graffiti by Gabriel Heimler",
                            ),
                
                # Titre H6
                html.H6("Choose Berlin Districts:", className="card-text"),
                
                # Zone vide
                html.Div(id="the_alert", # pour le callback
                         children=[], # données vides
                         ),
                
                # Menu déroulant
                dcc.Dropdown(id='district_chosen', # pour le callback
                             options=[{'label': d, "value": d} # valeurs du menu
                                      for d in df["District"].unique()],
                             value=["Lichtenberg", "Pankow", "Spandau"], # affichage
                             multi=True, # multiple affichage
                             style={"color": "#000000"}, # couleur du menu
                             ),
                
                # Ligne séparatrice
                html.Hr(),
                
                # Pour la nouvelle fenêtre à afficher
                modal
            ]
        ),
    ],
    color="light",
)

# Carte pour les cadres
graph_card = dbc.Card(
    [   
        # Carte
        dbc.CardBody(
            [   
                # Titre H4
                html.H4("Graffiti in Berlin 2012-2019", 
                        className="card-title", 
                        style={"text-align": "center"}),
                
                # Bouton d'exécution
                dbc.Button(
                    "About Berlin", # Texte affiché
                    id="popover-bottom-target", # pour le callback
                    color="info", # Couleur du bouton
                ),
                
                # Commentaire
                dbc.Popover(
                    [
                        # En-tête du commentaire
                        dbc.PopoverHeader("All About Berlin:"),
                        
                        # Corps principal du commentaire
                        dbc.PopoverBody(
                            "Berlin (/bɜːrˈlɪn/; German: [bɛʁˈliːn] is the capital and largest city of Germany by both area and population. Its 3,769,495 (2019) inhabitants make it the most populous city proper of the European Union. The city is one of Germany's 16 federal states. It is surrounded by the state of Brandenburg, and contiguous with Potsdam, Brandenburg's capital. The two cities are at the center of the Berlin-Brandenburg capital region, which is, with about six million inhabitants and an area of more than 30,000 km2, Germany's third-largest metropolitan region after the Rhine-Ruhr and Rhine-Main regions. (Wikipedia)"),
                    ],
                    id="popover", # pour le callback
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom", # commentaire placé en dessous du bouton
                    is_open=False, # True : commentaire toujours affiché
                ),
                
                # Graphique (vide)
                dcc.Graph(id='line_chart', # pour le callback
                          figure={}, # données vides
                          ),

            ]
        ),
    ],
    color="light",
)


# FRONT END ---------------------------------------------------------------------

# Instanciation de la librairie et thème de la page @
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configuration de la page @
app.layout = html.Div([
    
    dbc.Row([
        
        dbc.Col(image_card, width=3), # Cadre pour l'image, menu déroulant...
        
        dbc.Col(graph_card, width=8)], # Cadre pour le commentaire, graphique...
            
            justify="around")
])

# INTERACTION DES COMPOSANTS -----------------------------------------------------

# Affichage d'un commentaire en cliquant sur le bouton "About Berlin"
@callback(
    Output("popover", "is_open"), # Sortie : commentaire
    [Input("popover-bottom-target", "n_clicks")], # Entrée : Bouton d'exécution
    [State("popover", "is_open")], # State : commentaire
)
def toggle_popover(n, is_open):
    
    # Evite l'affichage automatique du commentaire dès ouverture de la page @
    if n:
        return not is_open
    
    return is_open

# MAJ du graphique linéaire selon les valeurs affichées dans le menu déroulant
# À défaut, message d'alerte affichée au menu déroulant
@callback(
    [Output("line_chart", "figure"), # Sortie : graphique
     Output("the_alert", "children")], # Sortie : message d'alerte
    [Input("district_chosen", "value")] # Entrée : menu déroulant
)
def update_graph_card(districts):
    
    # Si aucune donnée n'est affichée du menu déroulant :
    # alors pas de MAJ du graphique et message d'alerte
    if len(districts) == 0:
        return no_update, alert
    
    # Si au moins une valeur du menu déroulant est affichée :
    # alors MAJ du graphique
    else:
        # Filtre de la DF selon les valeurs affichées au menu déroulant
        df_filtered = df[df["District"].isin(districts)]
        
        # TCD par les champs 'Year' et 'District' : 
        # valeurs médianes du champ 'Graffiti'
        df_filtered = (df_filtered.groupby(["Year", "District"])[['Graffiti']]
                       .median().reset_index())
        
        # MAJ du graphique : graphique linéaire
        fig = px.line(df_filtered, # DF filtrée
                      x="Year", # axe des abscisses
                      y="Graffiti", # axe des ordonnées
                      color="District", # couleur des lignes à partir de ce champ
                      labels={"Graffiti": "Graffiti incidents (avg)"}
                      # Modification du titre de l'axe des ordonnées
                      ).update_traces(
                          mode='lines+markers', # lignes + points au graphique
                          )
        
        return fig, no_update # no_update : à la place du message d'alerte

# Ouverture d'une nouvelle fenêtre après avoir appuyé sur le bouton d'exécution
# "Add comment" et fermeture de cette nouvelle fenêtre après avoir appuyé sur
# le bouton d'exécution "Close"
@callback(
    Output("modal", "is_open"), # Sortie : Nouvelle fenêtre
    [Input("open", "n_clicks"), # Entrée : Bouton d'exécution
     Input("close", "n_clicks")], # Entrée : Bouton d'exécution
    [State("modal", "is_open")], # State : Nouvelle fenêtre
)
def toggle_modal(n1, n2, is_open):
    
    # Evite l'affichage automatique de la nouvelle fenêtre dès ouverture 
    # de la page @ ainsi que la fermeture automatique de cette nouvelle fenêtre
    # dès ouverture de cette fenêtre
    if n1 or n2:
        return not is_open
    
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
