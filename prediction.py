# ------------ This is a py file about AUTO ARIMA MODEL ---------------------------

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error
from pmdarima.metrics import smape
import pmdarima as pm
from pmdarima.arima import ndiffs


def forecast_one_step(model):
    fc, conf_int = model.predict(n_periods=1, return_conf_int=True)
    return (
        fc.tolist()[0],
        np.asarray(conf_int).tolist()[0])


def predict_tomorrow(df):
    train_len = int(df.shape[0] * 0.7)
    train_data, test_data = df[:train_len], df[train_len:]

    y_train = train_data['close'].values
    y_test = test_data['close'].values

    #print(f"{train_len} train samples")
    #print(f"{df.shape[0] - train_len} test samples")
    kpss_diffs = ndiffs(y_train, alpha=0.05, test='kpss', max_d=6)
    adf_diffs = ndiffs(y_train, alpha=0.05, test='adf', max_d=6)
    n_diffs = max(adf_diffs, kpss_diffs)

    auto = pm.auto_arima(y_train, d=n_diffs, seasonal=False, stepwise=True,
                         suppress_warnings=True, error_action="ignore", max_p=6,
                         max_order=None, trace=True)

    model_ = auto.order
    # print(f"Estimated differencing term: {n_diffs}")
    # Estimated differencing term: 1
    model = auto

    forecasts = []
    confidence_intervals = []

    for new_ob in y_test:
        fc, conf = forecast_one_step(model)
        forecasts.append(fc)
        confidence_intervals.append(conf)
        # Updates the existing model with a small number of MLE steps
        model.update(new_ob)

    mse_ = mean_squared_error(y_test, forecasts)
    smape_ = smape(y_test, forecasts)

    tomorrow, conf = forecast_one_step(model)


    # --------------------- Actual vs. Predicted --------------------------
    fig = go.Figure()
    fig.add_trace(
                go.Scatter(x=df.index, y=y_train, mode='lines', name='Training Data'))
    fig.add_trace(
                go.Scatter(x=test_data.index, y=forecasts, mode='lines', name='Predicted Price'))
    fig.add_trace(
                go.Scatter(x=test_data.index, y=y_test, mode='lines', name='Actual Price'))
    fig.update_layout(
            margin=dict(l=2, r=10, t=20, b=20),
        )

    return fig, model_, mse_, smape_, tomorrow
