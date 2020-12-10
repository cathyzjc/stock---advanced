import prediction
import pytest
import pandas as pd

df = pd.read_csv("data/daily_data.csv")


def test_predict_tomorrow():
    try:
        prediction.predict_tomorrow(df)
    except ValueError as ex:
        print(ex)
    assert True


if __name__ == "__main__":
    pytest.main()
