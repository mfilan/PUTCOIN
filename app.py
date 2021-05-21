import glob
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Read the data
frames = []
for f in glob.glob("data/coin_*.csv"):
    frames.append(pd.read_csv(f))
df = pd.concat(frames)
currencies = sorted(df['Name'].unique())
# Initialise the app
app = dash.Dash(__name__)
app.title = "PUTCOIN"
server = app.server

# Define the app
app.layout = html.Div(children=[
html.Div(children=[
    html.Img(src=app.get_asset_url('logo.png'), style={'height': '100%', 'width': '100%'}),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns[2:]
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        #column_selectable="single",
        #row_selectable="multi",
        #row_deletable=False,
        #selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(20, 20, 20)'
            }
        ],
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
    ),

    html.Div(id='datatable-row-ids-container')
    ]),

    html.Label('Choose cryptocurrency'),
    dcc.Dropdown(
        id='currency',
        options=[{'label': crypto, 'value': crypto} for crypto in currencies],
        value='Aave',
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Graph(
        id='candle',
        figure = px.line(template='plotly_dark').update_layout(
                {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    )
], style={'columnCount': 2})

# Callback
@app.callback(
    Output('candle', 'figure'),
    [Input('currency', 'value')]
)
def update_graph(val):
    sub_df = df.loc[df['Name'] == val]
    # Create figure with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]])

    # include candlestick with rangeselector
    fig.add_trace(
        go.Candlestick(
            x=sub_df['Date'],
            open=sub_df['Open'],
            high=sub_df['High'],
            low=sub_df['Low'],
            close=sub_df['Close'],
            name=val),
        secondary_y=True)

    # include a go.Bar trace for volumes
    fig.add_trace(
        go.Bar(
            x=sub_df['Date'],
            y=sub_df['Volume'],
            opacity=0.75,
            marker={'color': 'steelblue', 'line_color': 'steelblue'},
            name="Volume"),
        secondary_y=False)

    #include marketcap
    fig.add_trace(
        go.Scatter(
            x=sub_df['Date'],
            y=sub_df['Marketcap'],
            line=dict(color='orange'),
            name="Marketcap"),
        secondary_y=False)

    fig.layout.yaxis2.showgrid = False
    fig.update_layout(
                {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
                template='plotly_dark',
                barmode='group',
                bargroupgap=0,
                bargap=0)
    fig.update_yaxes(
        title_text="Volume and market capitalization",
        secondary_y=False)
    fig.update_yaxes(
        title_text="Price in USD",
        secondary_y=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


