import controls
import pytest
import pandas as pd

def test_update_a_share_list():
    try:
        controls.update_a_share_list()[0]
    except ValueError as ex:
        print(ex)
    assert {'label': 'sh.600000-浦发银行', 'value': 'sh.600000-浦发银行'}


def test_get_A_stock_list():
    try:
        len(controls.get_A_stock_list())
    except ValueError as ex:
        print(ex)
    assert 300


def test_share_dict_to_option():
    try:
        controls.share_dict_to_option({'sh.600000':'浦发银行'})
    except ValueError as ex:
        print(ex)
    assert 'sh.600000-浦发银行'


def test_split_share_to_code():
    # split options to get code
    try:
        controls.split_share_to_code('sh.600000-浦发银行')
    except ValueError as ex:
        print(ex)
    assert 'sh.600000'


def test_list_to_option_list():
    # quick create dropdown options from list
    try:
        controls.list_to_option_list(['sh.600000-浦发银行'])
    except ValueError as ex:
        print(ex)
    assert {"label": 'sh.600000-浦发银行', "value": 'sh.600000-浦发银行'}


def test_get_trend_df():
    try:
        controls.get_trend_df('sh.600000','2020-01-01','2020-07-07')
    except ValueError as ex:
        print(ex)
    assert True


def test_get_trend_week_df():
    try:
        controls.get_trend_week_df('sh.600000','2020-01-01','2020-07-07')
    except ValueError as ex:
        print(ex)
    assert True


def test_get_trend_month_df():
    try:
        controls.get_trend_month_df('sh.600000','2020-01-01','2020-07-07')
    except ValueError as ex:
        print(ex)
    assert True


def test_get_information():
    try:
        a = controls.get_information('sh.600000')
        print(a)
    except ValueError as ex:
        print(ex)
    assert ['sh.600000','浦发银行','1999-11-10','','Stock','Listed']


df = pd.read_csv("data/daily_data.csv")
@pytest.mark.parametrize('df, ma',
                         [
                             (df, [5, 10])
                         ])
def test_plot_candlestick(df, ma):
    fig = controls.plot_candlestick(df=df, ma=ma)
    fig.show()
    assert True

if __name__ == "__main__":
    pytest.main()

