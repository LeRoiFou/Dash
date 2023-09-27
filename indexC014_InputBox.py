"""
Lien : https://www.youtube.com/watch?v=VZ6IdRMc0RI&list=PLh3I780jNsiSvpGtPucq4yusBXVt3SL2Q&index=8
Cours : Input Box - Python Dash Plotly

Documentation sur le composant dcc.Input :
https://dash.plotly.com/dash-core-components/input

Date : 27-09-23
"""

from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px  

# DS ------------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("data/dup_bees.csv")

# Conversion du champ en type numérique
df['Value'] = pd.to_numeric(df['Value'])

# Assignation d'un dictionnaire
mapping = {'HONEY, BEE COLONIES, AFFECTED BY DISEASE - INVENTORY, MEASURED IN PCT OF COLONIES': 'Disease',
           'HONEY, BEE COLONIES, AFFECTED BY OTHER CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Other',
           'HONEY, BEE COLONIES, AFFECTED BY PESTICIDES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Pesticides',
           'HONEY, BEE COLONIES, AFFECTED BY PESTS ((EXCL VARROA MITES)) - INVENTORY, MEASURED IN PCT OF COLONIES': 'Pests_excl_Varroa',
           'HONEY, BEE COLONIES, AFFECTED BY UNKNOWN CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Unknown',
           'HONEY, BEE COLONIES, AFFECTED BY VARROA MITES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Varroa_mites'}

# Récupération uniquement des valeurs (et non les clés) du dictionnaire ci-avant
df['Data Item'] = df['Data Item'].map(mapping)

# Renommage des colonnes
df.rename(columns={'Data Item': 'Affected by', 
                   'Value': 'Percent of Colonies Impacted'}, inplace=True)

# Assignation d'un autre dictionnaire
state_codes = {
    'District of Columbia': 'dc', 'Mississippi': 'MS', 'Oklahoma': 'OK',
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
    'Nevada': 'NV', 'Maine': 'ME'}

# Récupération uniquement des valeurs (et non les clés) du dictionnaire ci-avant
df['state_code'] = df['State'].apply(lambda x: state_codes[x])

# Regroupement de certains champs avec une moyenne selon le champ 
# 'Percent of Colonies Impacted'
df = df.groupby(['State', 'State ANSI', 'Affected by', 'Year', 'state_code']
                )[['Percent of Colonies Impacted']].mean()

# Suppression des index
df.reset_index(inplace=True)

# CONFIGURATION DES COMPOSANTS ---------------------------------------------------

# Assignation d'une liste pour la zone de saisie
input_types = ['number', 'password', 'text', 'tel', 'email', 
               'url', 'search', 'hidden']

# FRONT END ----------------------------------------------------------------------

# Instanciation de la librarie
app = Dash(__name__)

# Configuration de la page @
app.layout = html.Div([
    
    html.Div([
        
        # Zones de saisies (compréhension de liste)
        dcc.Input(
            id=f'my_{x}', 
            type=x, 
            placeholder=f"insert {x}", # texte affiché par défaut
            debounce=False, # True -> appuyez sur Entrée pour MAJ des valeurs
            min=2015, # valeur minimum uniquement pour les champs numériques
            max=2019, # valeur maximum uniquement pour les champs numériques
            step=1, # incrémentation uniquement pour les champs numériques
            minLength=0, # nombre min de caractères uniquement pour les champs str
            maxLength=50, # nombre max de caractères uniquement pour les champs str
            autoComplete='on', # Autocomplétion : saisie texte intuitive par l'ordi
            disabled=False, # Verrouillage
            readOnly=False, # Lecture uniquement
            required=False, # True : exige une saisie dans la zone de texte
            size="20", # Longueur de la zone de texte
        ) for x in input_types
    ]),

    # Retour chariot
    html.Br(),

    # Graphique vide
    dcc.Graph(id="mymap"),

])


# INTERACTIONS ENTRE COMPOSANTS -----------------------------------------------

# MAJ de la carte graphique selon les éléments saisis dans la zone de texte
@callback(
    Output( # Sortie : graphique
        component_id='mymap', component_property='figure'),
    [Input( # Entrées : toutes les zones de saisies (compréhension de liste)
        component_id=f'my_{x}', component_property='value')
     for x in input_types
     ],
)
def update_graph(num_year, pwd_state, txt_state, tel_state, email_, url_, 
                 search_disease, hidden_input):
    
    # Valeurs par défaut
    if tel_state:
        tel_state = tel_state
    elif tel_state is None or len(tel_state) == 0:
        tel_state = 10

    # Valeurs par défaut
    if search_disease:
        search_disease = search_disease
    elif search_disease is None or len(search_disease) == 0:
        search_disease = "Disease"

    # Copie de la DF
    dff = df.copy()

    # Filtres opérés sur la DF
    dff = dff[dff['Year'] == num_year]
    dff = dff[dff['State'] != pwd_state]
    dff = dff[dff['State'] != txt_state]
    dff = dff[dff['State ANSI'] != int(tel_state)]
    dff = dff[dff['Affected by'] == search_disease]

    print("number: " + str(num_year))
    print("password: " + str(pwd_state))
    print("text: " + str(txt_state))
    print("telephone: " + str(tel_state))
    print("hidden: " + str(hidden_input))
    print("email: " + str(email_))
    print("url: " + str(url_))
    print("search: " + str(search_disease))
    print("---------------")

    # MAJ de la carte graphique
    beemap = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Percent of Colonies Impacted',
        hover_data=['State', 'Percent of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title=f'Bees affected by {search_disease}',
        template='plotly_dark',
        labels={'Percent of Colonies Impacted': '% of Bee Colonies'}
    )

    beemap.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}})

    beemap.update_traces(hovertemplate=
                         "<b>%{customdata[0]}</b><br><br>" +
                         "Percent of Colonies Impacted: %{customdata[1]:.3s}" +
                         "<extra></extra>",
                         )
    return beemap

# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
