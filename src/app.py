import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from __main__ import *
import CalculationsBis
import Controls
import Callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Twisted Mixed Multilayer Graphene: a Tunable K dot P Model Spectrum"

##################################################################
##################################################################
# CONFIGURATION for plot resolution and logo display
config = {
    'displaylogo': False,
    'toImageButtonOptions': {
    'format': 'svg', # one of png, svg, jpeg, webp
    'filename': 'tgkp-image',
    'height': 590,
    'width': 960,
    'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
  }
}

##################################################################
##################################################################
# LAYOUT

html.Script(src="iframeSizer.contentWindow.min.js")

app.layout = dbc.Container(
    [
        # title
        html.H1("Twisted Multilayer Graphene", className="display-5", style={'text-align':'center'}),
        html.H3("A Tunable KP Model Spectrum", className="display-5", style={'text-align':'center'}),

        html.P(dcc.Markdown(children=""" Visualize the bandstructure of twisted graphene systems with the parameters of your choice. 
        For more information, consult the [docs](https://drive.google.com/file/d/1Y9lRb0_3BB3XxXh6lz3DgkL2reWMv5hD/view?usp=sharing). """),
        className="lead", style={'text-align':'center'}),

        html.Hr(),

        # middle
        dbc.Row([
            dbc.Col(Controls.Card, md=4),
            dbc.Col(dbc.Card([dcc.Graph(id="RawDataGraph", config=config)], body=True),md=8),
        ], align="center"),

        html.Hr(),
        
        # footer
        dbc.Card([
            dbc.Row(
                [
                    dbc.Col(dcc.Markdown(children="""Questions? **[Send me an e-mail](mailto:leo.goutte@mail.mcgill.ca)** 

Source code: [![](https://img.icons8.com/material-sharp/2x/github.png)](https://github.com/leogoutte/tmg)

Made by: **Leo Goutte** and **QuanSheng Wu**
                
For: **Condensed matter physicists in a hurry**"""), width=9),
                    dbc.Col(html.Div()),
                    dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Logo_EPFL.svg/1024px-Logo_EPFL.svg.png",width="111",height="32"), width=2),
                ]
            ),
        ],body=True, color='light'),
        html.Hr(),
        html.Div(**{'data-iframe-height':''}),
    ],
    fluid=True,
)
##################################################################
##################################################################
# CALLBACKS

# schematic
@app.callback(
    Output('schematic', 'src'),
    Input('stackingvalue', 'value'))
def update_figure(stacking):
    encoded_image = Callbacks.schematic(stacking)
    return 'data:image/png;base64,{}'.format(str(encoded_image)[1:].replace("'","")) # remove 'b'

# graph
@app.callback(
    [Output('RawDataGraph', 'figure'),
    Output('loading-output', 'children')],
    Input('submit-button-state', 'n_clicks'),
    State('stackingvalue', 'value'),
    State('thetavalue', 'value'),
    State('tAAvalue', 'value'),
    State('tABvalue', 'value'),
    State('ElectricFieldvalue', 'value'),
    State('Nvalue', 'value'),
    State('bandsvalue', 'value'))
def update_figure(n_clicks,stacking,theta,tAA,tAB,ElectricField,N,bands):
    fig = Callbacks.fig(stacking,theta,tAA,tAB,ElectricField,N,bands)
    # must wrap to satisfy two outputs
    return [fig, None] 

# download
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True)
def func(n_clicks):
    dataframe = Callbacks.dataframe()
    return dcc.send_data_frame(dataframe.to_csv, "tgkp-data.csv")


#############################################################################
# RUN ON SERVER
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=5000,debug=True)
