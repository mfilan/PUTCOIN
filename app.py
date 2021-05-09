import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
