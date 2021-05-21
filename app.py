import glob
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go

# Read the data
frames = []
currencies = []
for f in glob.glob("data/coin_*.csv"):
    currencies.append(f[10:-4])
    frames.append(pd.read_csv(f))
df = pd.concat(frames)
currencies = sorted(currencies)
# Initialise the app
app = dash.Dash(__name__)
app.title = "PUTCOIN"
server = app.server

# Define the app
app.layout = html.Div([

    html.Img(src=app.get_asset_url('logo.png'), style={'height':'100%', 'width':'100%'}),

    html.Label('Choose currency'),
    dcc.Dropdown(
        id='my_dropdown',
        options = [{'label': crypto, 'value': crypto} for crypto in currencies],
        value='Currency',
        multi=False,
        clearable=False,
        style={"width": "50%"}
    ),
    dcc.Graph(id='timeseries',
        config={'displayModeBar': False},
        animate=True,
        figure=px.line(df,
            x='Date',
            y='Close',
            color='Symbol',
            template='plotly_dark').update_layout(
            {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    ),

    html.Label('Text Input'),
    dcc.Input(value='MTL', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'columnCount': 2})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
