from dash import dcc, html
from dash.dependencies import Output, Input
import dash
from load_data import StockDataLocal
import plotly_express as px
from time_filtering import filter_time
import pandas as pd
import dash_bootstrap_components as dbc

# module variables

# create an object of type StockDataLocal so that we can load data
stock_data_object = StockDataLocal()


symbol_dict = {"AAPL": "Apple", "NVDA": "Nvidia",
               "TSLA": "Tesla", "IBM": "IBM"}

# stock_symbol: [daily_df, intradaily_df]
df_dict = {symbol: stock_data_object.stock_dataframe(
    symbol) for symbol in symbol_dict}


stock_options_dropdown = [{"label": name, "value": symbol}
                          for symbol, name in symbol_dict.items()]

# ohlc - Open, High, Low, Close
ohlc_options = [{"label": option.capitalize(), "value": option}
                for option in ["open", "high", "low", "close"]]

slider_marks = {i: mark for i, mark in enumerate(
    ["1 day", "1 week", "1 month", "3 months", "1 year", "5 year", "Max"])}

stylesheets = [dbc.themes.MATERIA]
# creates a Dash App
app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

server = app.server  # needed for Heroku to connect to



app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1('Stocks viewer',
                    className='card-title text-dark mx-3')
        ])
    ], className="mt-4"),

    dbc.Row(className='mt-4', children=[
        dbc.Col(
            # responsivity
            html.P("Choose a stock"), xs="12", sm="12", md="6", lg="4", xl={"size": 1, "offset": 2},
            className="mt-1"
        ),
        dbc.Col(
            dcc.Dropdown(id='stock-picker-dropdown', className='',
                         options=stock_options_dropdown,
                         value='AAPL',
                         placeholder='Apple'), xs="12", sm="12", md="12", lg="4", xl="3"),

        dbc.Col([
            dbc.Card([
                dcc.RadioItems(id='ohlc-radio', className="m-1",
                                  options=ohlc_options,
                                  value='close'
                               ),
            ])
        ], xs="12", sm="12", md="12", lg='4', xl="3"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="stock-graph"),
            dcc.Slider(id='time-slider',
                       min=0,
                       max=6,
                       step=None,
                       value=2,
                       marks=slider_marks
                       ),
        ], lg={"size": "6", "offset": 1}, xl={"size": "6", "offset": 1}),

        dbc.Col([
            dbc.Row(
                dbc.Card([
                    html.H2("Highest value", className="h5 mt-3 mx-3"),
                    html.P(id="highest-value", className="text-success h1 mx-2")
                ]), className="mt-5 h-25"
            ),
            dbc.Row(
                dbc.Card([
                    html.H2("Lowest value", className="h5 mt-3 mx-3"),
                    html.P(id="lowest-value", className="text-danger h1 mx-2")
                ]),
                className="mt-5 h-25"
            ),
        ], sm="5", md="3", lg="3", xl="2", className="mt-5 mx-5"),

        html.Footer([
            html.H3("Stock viewer 2021", className="h6"),
            html.P("Dashboard av Kokchun Giang")],
            className="navbar fixed-bottom")

    ]),

    # stores an intermediate value on the clients browser for sharing between callbacks
    dcc.Store(id="filtered-df"),
], fluid=True)


@app.callback(Output("filtered-df", "data"), Input("stock-picker-dropdown", "value"),
              Input("time-slider", "value"))
def filter_df(stock, time_index):
    """Filters the dataframe and stores it intermediary for usage in callbacks
    Returns:
        json object of filtered dataframe
    """
    dff_daily, dff_intraday = df_dict[stock]

    dff = dff_intraday if time_index <= 2 else dff_daily

    days = {i: day for i, day in enumerate([1, 7, 30, 90, 365, 365*5])}

    dff = dff if time_index == 6 else filter_time(dff, days=days[time_index])

    return dff.to_json()

# when something changes in the input component, the code in function below will run and update the output component
# the components are connected through their id


@app.callback(
    Output("stock-graph", "figure"),
    Input("filtered-df", "data"),
    Input("ohlc-radio", "value"),
    Input("stock-picker-dropdown", "value")
)
def update_graph(json_df, ohlc, stock):
    """Updates graph based on different unputs"""

    dff = pd.read_json(json_df)

    fig = px.line(dff, x=dff.index,
                  y=ohlc, title=symbol_dict[stock])

    # TODO: Add figure settings to make graph look nice

    return fig


@app.callback(
    Output("highest-value", "children"),
    Output("lowest-value", "children"),
    Input("filtered-df", "data"),
    Input("ohlc-radio", "value")
)
def highest_lowest_value(json_df, ohlc):
    dff = pd.read_json(json_df)
    highest_value = f"{dff[ohlc].max():.2f} USD"
    lowest_value = f"{dff[ohlc].min():.2f} USD"
    return highest_value, lowest_value


if __name__ == "__main__":
    app.run_server(debug=True)
