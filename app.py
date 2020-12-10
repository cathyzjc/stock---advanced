import dash
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go # 画出趋势图
from dash.exceptions import PreventUpdate
import pandas as pd
from prediction import predict_tomorrow, forecast_one_step
from controls import update_a_share_list, get_A_stock_list, \
    write_A_stock_list_to_csv, share_dict_to_option, split_share_to_code, read_df, \
    list_to_option_list, get_trend_df, get_trend_week_df, get_trend_month_df, plot_candlestick, get_information


# --------------- Part One  Some Setups -------------------------------------------
# create dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# ID definitions
id_button_update_a_share_list = 'id-button-update-a-share-list'
id_dpl_share_code = 'id-dpl-share-code'
id_button_query_trend = 'id-button-query-trend'
id_graph_hist_trend_graphic = 'id-graph-hist-trend-graphic'
id_graph_hist_trend_week_graphic = 'id-graph-hist-trend-week-graphic'
id_graph_hist_trend_month_graphic = 'id-graph-hist-trend-month-graphic'
id_stock_code = 'id-stock-code'
id_stock_name = 'id-stock-name'
id_ipo_date = 'id-ipo-date'
id_out_date = 'id-out-date'
id_stock_type = 'id-stock-type'
id_stock_status = 'id-stock-status'
id_web = 'id-web'
id_check_list_1 = 'id-check-list-1'
id_check_list_2 = 'id-check-list-2'
id_check_list_3 = 'id-check-list-3'
id_graph_predict = 'id-graph-predict'
id_button_predict = 'id-button-predict'
id_model = 'id-model'
id_mse = 'id-mse'
id_smape = 'id-smape'
id_tomorrow = 'id-tomorrow'

# default file to save stock codes list
A_STOCK_FILE = 'data/a_stock_list.csv'

# default time setup
today = datetime.today().date()


# --------------- Part Two  Dash Layout Components -------------------------------------------
# Button 1: update list button
# Use this button to download newest list of stocks. Do not need to use this button everytime

update_a_share_button = dbc.Button(
    id=id_button_update_a_share_list,
    color='info',
    children='Update Newest List', outline=True)

# Dropdown List:
# Contains all of the stocks to pick. The default value is sh.600000
select_share = dcc.Dropdown(
    id=id_dpl_share_code,
    options=update_a_share_list(),
    value='sh.600000-浦发银行'
)

# Botton 2: Submit button
# The main button of this project. Click and get more information of the stock.
query_button = dbc.Button(
    "Submit",
    color="warning",
    className="mr-1",
    id=id_button_query_trend,
    outline=False)

# Button 3: Submit button
# The main button of this project. Click and get more information of the stock.
predict_button = dbc.Button(
    "Predict",
    color="info",
    className="mr-1",
    id=id_button_predict,
    outline=False,
    size="lg",
    block=True)


# Checklist 1
# To add moving average trend on the daily candlestick plot
checklist1 = dcc.Checklist(
    options=[
        {'label': '5 days Moving Average', 'value': '5'},
        {'label': '10 days Moving Average', 'value': '10'},
        {'label': '20 days Moving Average', 'value': '20'},
        {'label': '30 days Moving Average', 'value': '30'},
    ],
    value=['5', '10'],
    id=id_check_list_1,
    labelStyle={'margin': '20px'},
)


# Checklist 2
# To add moving average trend on the weekly candlestick plot
checklist2 = dcc.Checklist(
    options=[
        {'label': '5 days Moving Average', 'value': '5'},
        {'label': '10 days Moving Average', 'value': '10'},
        {'label': '20 days Moving Average', 'value': '20'},
        {'label': '30 days Moving Average', 'value': '30'},
    ],
    value=['5', '10'],
    id=id_check_list_2,
    labelStyle={'margin': '20px'},
)


# Checklist 3
# To add moving average trend on the monthly candlestick plot
checklist3 = dcc.Checklist(
    options=[
        {'label': '5 days Moving Average', 'value': '5'},
        {'label': '10 days Moving Average', 'value': '10'},
        {'label': '20 days Moving Average', 'value': '20'},
        {'label': '30 days Moving Average', 'value': '30'},
    ],
    value=['5', '10'],
    id=id_check_list_3,
    labelStyle={'margin': '20px'},
)

# To combine first part together, and make a better layout
select_share_row = dbc.Container(
    [
        html.H3(today),
        html.Br(),
        html.H3('Please Select A Stock:'),
        dbc.Row(
            [
                dbc.Col(
                    [select_share],
                   ),
                dbc.Col(
                    [update_a_share_button],
                    )]),
        html.Br(),
        dbc.Row(
            [
                #dbc.Col(
                #    [date_pick],
                #    className='col-5'),
                dbc.Col(
                    [query_button],
                    )])])

# Figure 1: get default figure
default_fig = go.Figure()

# Figure 2: candlestick plots
# Use Tabs to organize the plots
graphic_div = dcc.Tabs([
    dcc.Tab(label='1 Day Candle', children=[
        dbc.Row(checklist1, style={'marginLeft': 60}),
        dcc.Graph(figure=default_fig, id=id_graph_hist_trend_graphic,style={'marginLeft': 40,'marginRight': 40,})
    ]),
    dcc.Tab(label='1 Week Candle', children=[
        dbc.Row(checklist2, style={'marginLeft': 60}),
        dcc.Graph(figure=default_fig, id=id_graph_hist_trend_week_graphic,style={'marginLeft': 40,'marginRight': 40,})
    ]),
    dcc.Tab(label='1 Month Candle', children=[
        dbc.Row(checklist3, style={'marginLeft': 60}),
        dcc.Graph(figure=default_fig, id=id_graph_hist_trend_month_graphic,style={'marginLeft': 40,'marginRight': 40,})
    ]),
], style={'marginLeft': 60,'marginRight': 60, 'marginTop': 10, 'marginBottom': 60})


# Figure 3: Prediction Plots
# This plot shows the result of AUTO ARIMA model
graph_predict = dcc.Graph(figure=default_fig, id=id_graph_predict, style={'marginLeft': 40,'marginRight': 40,})


# Table 1: Stock information
# This table contains basic information of the stock
row1 = html.Tr([html.Td("Name in Chinese"), html.Td(id=id_stock_name)])
row2 = html.Tr([html.Td("IPO Date"), html.Td(id=id_ipo_date)])
row3 = html.Tr([html.Td("Out Date"), html.Td(id=id_out_date)])
row4 = html.Tr([html.Td("Type"), html.Td(id=id_stock_type)])
row5 = html.Tr([html.Td("Status"), html.Td(id=id_stock_status)])

table_body = [html.Tbody([row1, row2, row3, row4, row5])]


# Table 2: Prediction Model information
# This table contains basic information of the ARIMA prediction model
row6 = html.Tr([html.Td("Model"), html.Td(id=id_model)])
row7 = html.Tr([html.Td("MSE"), html.Td(id=id_mse)])
row8 = html.Tr([html.Td("SMAPE"), html.Td(id=id_smape)])

table_body_2 = [html.Tbody([row6, row7, row8])]


# Finally, Fully Layout!
app.layout = html.Div([

    # Row 1 (Header)

    html.Div(style={'backgroundColor': '#528DA4'}, children=[
        dbc.Row([html.Br([])]),
        dbc.Row([html.H1('Constituents of CSI 300 ', style={'color':'#FFFFFF'})],style={'marginLeft': 40, 'marginTop': 30, 'marginBottom': 30}),
        dbc.Row([html.H6('CSI 300 : A market index designed to replicate top 300 stocks traded on the Shanghai '
                                'and the Shenzhen Stock Exchange.', style={'color':'#E1E1E1'}),
                 html.H6('This page shows the constituents of CSI 300', style={'color': '#E1E1E1'})
                 ],style={'marginLeft': 40, 'marginBottom': 40}),
        dbc.Row([html.Br([])],style={'marginLeft': 40, 'marginTop': 40, 'marginBottom': 40}),
      ]),

    # Row 2 (Contains Functions to choose stock and submit)

    dbc.Row([
        dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [select_share_row]
                        ),
                        )
                ], width=7),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                 [
                    html.H4(id=id_stock_code, className="card-title"),
                    dbc.Table(table_body, bordered=True),
                    dbc.CardLink("More Information on Yahoo Finance", id=id_web),
                 ]
                ),
                )
        ], width=5),
    ],style={'marginLeft': 60,'marginRight': 60, 'marginTop': 60, 'marginBottom': 60}),

    # Row 3 (Candlestick plots)

    graphic_div,

    # Row 4 (Header of the Prediction Part)

    html.Div(children=[
        dbc.Row([html.Br([])]),
        dbc.Row([html.Br([])]),
        dbc.Row([html.H1('Prediction Model')],style={'marginLeft': 60, 'marginTop': 70, 'marginBottom': 30}),
        dbc.Row([html.Br([])],style={'marginLeft': 40, 'marginBottom': 40}),
      ]),

    # Row 5 (Prediction Model)

    dbc.Row([
        dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            predict_button,
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.H4(id=id_tomorrow, className="card-title"),
                            html.Br([]),
                            dbc.Table(table_body_2, bordered=True),

                        ]
                        ),
                        )
                ], width=3),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([graph_predict]
                ),
                )
        ], width=9),
    ],style={'marginLeft': 60,'marginRight': 60, 'marginTop': 60, 'marginBottom': 60}),


])


# --------------- Part Three  Callback Functions -------------------------------------------


# Function of Daily candlestick plot


@app.callback(
    Output(id_graph_hist_trend_graphic, 'figure'),
    [Input(id_button_query_trend, 'n_clicks'),
     Input(id_check_list_1, 'value')],
    [State(id_dpl_share_code, 'value')]
)
def update_output_div(query, ma, share):
    if query is not None:
        share_code = split_share_to_code(share)
        start_date = datetime.today().date() - timedelta(days=120)
        end_date = datetime.today().date()
        return plot_candlestick(
            get_trend_df(
                share_code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')), ma)
    else:
        raise PreventUpdate


# Function of Weekly candlestick plot


@app.callback(
    Output(id_graph_hist_trend_week_graphic, 'figure'),
    [Input(id_button_query_trend, 'n_clicks'),
     Input(id_check_list_2, 'value')],
    [State(id_dpl_share_code, 'value'),]
)
def update_output_div(query, ma, share):
    if query is not None:
        share_code = split_share_to_code(share)
        start_date = datetime.today().date() - timedelta(days=600)
        end_date = datetime.today().date()
        return plot_candlestick(
            get_trend_week_df(
                share_code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')), ma)
    else:
        raise PreventUpdate


# Function of Monthly candlestick plot


@app.callback(
    Output(id_graph_hist_trend_month_graphic, 'figure'),
    [Input(id_button_query_trend, 'n_clicks'),
     Input(id_check_list_3, 'value')],
    [State(id_dpl_share_code, 'value')]
)
def update_output_div(query, ma, share):
    if query is not None:
        share_code = split_share_to_code(share)
        start_date = datetime.today().date() - timedelta(days=2400)
        end_date = datetime.today().date()
        return plot_candlestick(
            get_trend_month_df(
                share_code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')), ma)
    else:
        raise PreventUpdate


# Function of Prediction Plot and model information


@app.callback(
    Output(id_graph_predict, 'figure'),
    Output(id_model, 'children'),
    Output(id_mse, 'children'),
    Output(id_smape, 'children'),
    Output(id_tomorrow, 'children'),
    [Input(id_button_predict, 'n_clicks')],
    [State(id_dpl_share_code, 'value')]
)
def update_predict(query, share):
    if query is not None:
        share_code = split_share_to_code(share)
        start_date = datetime.today().date() - timedelta(days=720)
        end_date = datetime.today().date()
        df = get_trend_df(
                share_code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'))
        fig, model_, mse_, smape_, tomorrow = predict_tomorrow(df)
        model_output = 'ARIMA Model. p = {}, d = {} , q = {}'.format(model_[0], model_[1], model_[2])
        tmr_output = ' Tomorrow Predicted: %s' % round(tomorrow,2)
        return fig, model_output, round(mse_, 4), round(smape_, 4), tmr_output
    else:
        raise PreventUpdate


# Function of stock model information


@app.callback(
    Output(id_stock_code, 'children'),
    Output(id_stock_name, 'children'),
    Output(id_ipo_date, 'children'),
    Output(id_out_date, 'children'),
    Output(id_stock_type, 'children'),
    Output(id_stock_status, 'children'),
    Output(id_web, 'href'),
    [Input(id_button_query_trend, 'n_clicks')],
    [State(id_dpl_share_code, 'value'),]
)
def update_information(query, share):
    if query is not None:
        share_code = split_share_to_code(share)
        comp = share_code.split(".")
        if comp[0] == 'sh':
            comp[0] = 'ss'
        stock_web = comp[1] + '.' + comp[0]
        web = "https://finance.yahoo.com/quote/%s" % stock_web
        a, b, c, d, e, f = get_information(share_code)
        return a, b, c, d, e, f, web
    else:
        raise PreventUpdate

# Download newest list of stocks


@app.callback(
    Output(id_dpl_share_code, 'options'),
    [Input(id_button_update_a_share_list, 'n_clicks')]
)
def update_output_div(update):
    if update is not None:
        write_A_stock_list_to_csv(A_STOCK_FILE)
        return update_a_share_list()
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
