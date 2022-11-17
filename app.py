import dash
from dash import Dash, html, dcc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Output, Input, State


import datetime
from dateutil.relativedelta import relativedelta

import yfinance as yf
import plotly.graph_objs as go



start = datetime.datetime.today() - relativedelta(years=2)
end = datetime.datetime.today()

app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Input(id="stock-input", value="SPY", type='text'),
        html.Button(id="summit-button", n_clicks=0, children="Submit")
    ]),

    html.Div([
        html.H2("Stock App")
    ], className="banner"),
    html.Div([
        html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className='first'),

    ]),
])
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


@app.callback(dash.dependencies.Output("graph_close", "figure"),
              [Input("summit-button", "n_clicks")],
              [State("stock-input", "value")])
def update_fig(n_clicks, input_value):
    df = yf.download(input_value, start=start, end=end)

    data = []

    trace1 = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])
    data.append(trace1)

    layout11 = go.Layout(
        title=input_value,
        title_x=0.5,
        titlefont=dict(
            color='Black',
            size=20
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(
                color='white'
            )
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(
                color='white'
            )
        )
    )
    layout = {"title": input_value}

    return {
        "data": data,
        "layout": layout11
    }
app.run_server(debug=True)
