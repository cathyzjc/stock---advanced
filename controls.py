import plotly.graph_objects as go # 画出趋势图
import pandas as pd
import baostock as bs

# default file to save stock codes list
A_STOCK_FILE = 'data/hs300_stocks.csv'


def update_a_share_list():
    # display a stock share list from csv
    a_share_list_df = pd.read_csv(A_STOCK_FILE, index_col='code')
    share_dict = a_share_list_df.to_dict()['code_name']
    return share_dict_to_option(share_dict)


def get_A_stock_list():
    bs.login()
    rs = bs.query_hs300_stocks()
    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
    # 登出系统
    bs.logout()
    result.set_index('code', inplace=True)
    result = result.drop(columns=['updateDate'])
    return result


def write_A_stock_list_to_csv(file):
    # sync to csv
    share_df = get_A_stock_list()
    share_df.to_csv(file)


def share_dict_to_option(share_dict):
    # convert name and code to options
    name_list = [str(key) + '-' + str(value)
                 for key, value in share_dict.items()]
    return list_to_option_list(name_list)


def split_share_to_code(share):
    # split options to get code
    code = share.split('-')[0]
    return code


def list_to_option_list(list):
    # quick create dropdown options from list
    return [{"label": i, "value": i} for i in list]


def get_trend_df(code, start_date, end_date):
    # get history tend by code,start_date,end_dates
    bs.login()
    rs = bs.query_history_k_data_plus(code,
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date=start_date, end_date=end_date,
    frequency="d", adjustflag="3") # adjustflag="3"默认不复权
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['date'] = pd.to_datetime(result['date'], format='%Y-%m-%d')
    result.set_index('date', inplace=True)
    result.sort_index(inplace=True)  # sort result by date (datetime)
    bs.logout()
    return result


def get_trend_week_df(code, start_date, end_date):
    # get history tend by code,start_date,end_dates
    bs.login()
    rs = bs.query_history_k_data_plus(code,
    "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    start_date=start_date, end_date=end_date,
    frequency="w", adjustflag="3") # adjustflag="3"默认不复权
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['date'] = pd.to_datetime(result['date'], format='%Y-%m-%d')
    result.set_index('date', inplace=True)
    result.sort_index(inplace=True)  # sort result by date (datetime)
    bs.logout()
    return result


def get_trend_month_df(code, start_date, end_date):
    # get history tend by code,start_date,end_dates
    bs.login()
    rs = bs.query_history_k_data_plus(code,
    "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    start_date=start_date, end_date=end_date,
    frequency="m", adjustflag="3") # adjustflag="3"默认不复权
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['date'] = pd.to_datetime(result['date'], format='%Y-%m-%d')
    result.set_index('date', inplace=True)
    result.sort_index(inplace=True)  # sort result by date (datetime)
    bs.logout()
    return result


def read_df(file):
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df


def get_information(code):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    # 获取证券基本资料
    rs = bs.query_stock_basic(code=code)
    # 打印结果集
    data_list = []
    type = {'1': 'Stock', '2': 'Index', '3': 'Others'}
    status = {'1': 'Listed', '2': 'Delisted'}
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    bs.logout()
    data = data_list[0]
    stock_code = data[0]
    stock_name = data[1]
    ipoDate = data[2]
    outDate = data[3]
    stock_type = type[data[4]]
    stock_status = status[data[5]]
    return stock_code, stock_name, ipoDate, outDate, stock_type, stock_status


def plot_candlestick(df, ma):
    # plot candlestick
    # customize the color to China Stock
    df['ma5'] = df.close.rolling(window=5).mean()
    df['ma10'] = df.close.rolling(window=10).mean()
    df['ma20'] = df.close.rolling(window=20).mean()
    df['ma30'] = df.close.rolling(window=30).mean()
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing=dict(
                    line=dict(
                        color="#CC0000")),
                decreasing=dict(
                    line=dict(
                        color="#25ae25")),
            )])
    if '5' in ma:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['ma5'], mode='lines', name='moving average = 5'))
    if '10' in ma:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['ma10'], mode='lines', name='moving average = 10'))
    if '20' in ma:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['ma20'], mode='lines', name='moving average = 20'))
    if '30' in ma:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['ma30'], mode='lines', name='moving average = 30'))
    fig.update_layout(
        margin=dict(l=2, r=10, t=20, b=20),
    )  # change the layout of figure
    return fig