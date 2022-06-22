# This library is used to initialize the dash application.
import dash

# This library is used to add graphs,other visual components.
import dash_core_components as dcc

# This library is used to include html tags.
import dash_html_components as html

# For data manipulation and mathematical operations.
import pandas as pd

# Reading the csv file.
from dash import Output, Input

data = pd.read_csv("indexData.csv")

# Manipulating the date.
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

# Initialising application.
app = dash.Dash(__name__)

# Defining the app layout.
app.layout = html.Div(

    children=[

        html.H1(children="Stock Exchange Analytics", ),
        html.P(
            children="Analyzing day wise opening and closing prices of indexes.",
        ),
        html.Div(
            children=[
                html.Div(
                    children="Date Range",
                    className="menu-title"
                ),
                dcc.DatePickerRange(
                    id="date-range",
                    min_date_allowed=data.Date.min().date(),
                    max_date_allowed=data.Date.max().date(),
                    start_date=data.Date.min().date(),
                    end_date=data.Date.max().date(),
                ),
            ]
        ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data["Date"],
        #                 "y": data["High"],
        #                 "type": "lines",
        #             },
        #         ],
        #         "layout": {"title": "Day-wise highest prices of indexes"},
        #     },
        # ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data["Date"],
        #                 "y": data["Low"],
        #                 "type": "lines",
        #             },
        #         ],
        #         "layout": {"title": "Day-wise lowest prices of indexes"},
        #     },
        # ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data["Date"],
        #                 "y": data["Close"],
        #                 "type": "lines",
        #             },
        #         ],
        #         "layout": {"title": "Day-wise closing prices of indexes"},
        #     },
        # ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data["Date"],
        #                 "y": data["Open"],
        #                 "type": "lines",
        #             },
        #         ],
        #         "layout": {"title": "Day-wise opening prices of indexes"},
        #     },
        # ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="open-price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="close-price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


#     ]
# )

# Defining the callback layout
@app.callback(
    [Output("open-price-chart", "figure"), Output("close-price-chart", "figure")],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(start_date, end_date):
    mask = (
            (data.Date >= start_date)
            & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    open_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Open"],
                "type": "lines",
                "hover-template": "$%{y:.2f}",
            },
        ],
        "layout": {
            "title":
            {
                "text": "Opening Price of Indexes",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixed-range": True},
            "yaxis": {"tick-prefix": "$", "fixed-range": True},
            "colorway": ["#17B897"],
        },
    }
    close_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Close"],
                "type": "lines",
            },
        ],
        "layout": {
            "title":
            {
                "text": "Closing Price of indexes.",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixed-range": True},
            "yaxis": {"fixed-range": True},
            "colorway": ["#E12D39"],
        },
    }
    return open_price_chart_figure, close_price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
