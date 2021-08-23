import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

###########################################################
# POPOVER

stacking_popover = [
    dbc.PopoverHeader("Stacking"),
    dbc.PopoverBody("Set stacking configuration. A list of 'A', 'B', or 'C' layers with the single twist denoted by '-'."),
]

theta_popover = [
    dbc.PopoverHeader("Twist angle θ"),
    dbc.PopoverBody("The relative twist angle in degrees (°)."),
]

tAA_popover = [
    dbc.PopoverHeader("AA region tunneling"),
    dbc.PopoverBody("The amplitude of tunneling energy between AA regions in meV."),
]

tAB_popover = [
    dbc.PopoverHeader("AB region tunneling"),
    dbc.PopoverBody("The amplitude of tunneling energy between AB regions in meV."),
]

efield_popover = [
    dbc.PopoverHeader("Electric field"),
    dbc.PopoverBody("Strength of the perpendicular electric field in meV/Å. Positive (negative) values are parallel to +z (-z)."),
]

N_popover = [
    dbc.PopoverHeader("Truncation range"),
    dbc.PopoverBody("Largest Moiré vectors considered for the computation, in units of a single Moiré vector. Size of Moiré zone."),
]

bands_popover = [
    dbc.PopoverHeader("Number of bands"),
    dbc.PopoverBody("Number of energy bands to compute."),
]

###########################################################
# CARD

Card = dbc.Card([
    html.H4("Physical parameters", className="card-title"),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Stacking (A, B, C; - indicates twist)", id="stackingLabel"),
                dbc.Popover(stacking_popover,id='stackinghover',target='stackingLabel',trigger='hover')
                ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='stackingvalue', type='text', value="A-B"), md=12),
            dbc.Col(html.Img(id='schematic'), md=12),
        ]),
    ]), 

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([dbc.Label("θ (°)", id="thetaLabel"), 
            dbc.Popover(theta_popover,id='thetahover',target='thetaLabel',trigger='hover')
            ]), md=8)], justify="between"),
        # un-comment for slider functionality
        # dbc.Row([
        #     dbc.Col(html.Div([
        #         dcc.Slider(
        #             id="Input1value",
        #             min=0,
        #             max=2,
        #             step=0.05,
        #             value=1,
        #             marks={
        #                 0:'0',
        #                 0.5:'0.5',
        #                 1:'1',
        #                 1.05:'*',
        #                 1.5:'1.5',
        #                 2:'2'
        #             })
        #         ])),
        # ]),
        # html.Div(id="slider-output-container")
        dbc.Row([
            dbc.Col(dcc.Input(id='thetavalue', type='number', step=0.01, value=1.08), md=12),
        ]),
    ]),


    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("AA tunneling (meV)", id="tAALabel"),
                dbc.Popover(tAA_popover,id='tAAhover',target='tAALabel',trigger='hover')
            ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='tAAvalue', type='number', value=110.7), md=12),
        ]),
    ]),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("AB tunneling (meV)", id="tABLabel"),
                dbc.Popover(tAB_popover,id='tABhover',target='tABLabel',trigger='hover')
            ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='tABvalue', type='number', value=110.7), md=12),
        ]),
    ]),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Electric field (meV/Å)", id="ElectricfieldLabel"),
                dbc.Popover(efield_popover,id='Electricfieldhover',target='ElectricfieldLabel',trigger='hover')
            ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='ElectricFieldvalue', type='number', value=0.0, step=0.1), md=12),
        ]),
    ]),

    
    html.H4("Computational parameters", className="card-title"),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Truncation range", id="NLabel"),
                dbc.Popover(N_popover,id='Nhover',target='NLabel',trigger='hover')
            ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='Nvalue', type='number', step=1, value=3), md=12),
        ]),
    ]),

    dbc.FormGroup([
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Number of bands", id="bandsLabel"),
                dbc.Popover(bands_popover,id='bandshover',target='bandsLabel',trigger='hover')
            ]), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='bandsvalue', type='number', value=20, step=1), md=12),
        ]),
    ]),

    # Submit button
    dbc.Row([
        dbc.Col(
            dbc.ButtonGroup([
                dbc.Button("Update", id='submit-button-state', color='danger', n_clicks=0),
                dbc.Button(children="Download", id="btn_csv", color='dark'),
                dcc.Download(id="download-dataframe-csv")
            ]),

        ),
        dbc.Col(
            dbc.Button(children=dcc.Loading(id='loading-output',type='circle',color='#C0291D'),
                color="light",
                disabled=True)
        ),
    ]),

], body=True, color='light')