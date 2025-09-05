from __future__ import annotations
import pickle
import pandas as pd
from arch import arch_model


def fit_garch11(r: pd.Series, dist: str = "t"):
    """
    r: log returns in decimal. We multiply by 100 for arch (percent units).
    dist: 'normal' | 't' | 'skewt'
    """
    am = arch_model(r * 100, mean="Constant", vol="GARCH", p=1, q=1, dist=dist)
    res = am.fit(disp="off")
    return res


def save_model(res, path: str):
    """
    Save fitted ARCH/GARCH model to pickle file.
    """
    with open(path, "wb") as f:
        pickle.dump(res, f)


def load_model(path: str):
    """
    Load a previously saved ARCH/GARCH model from pickle file.
    """
    with open(path, "rb") as f:
        return pickle.load(f)


def forecast_volatility(model, horizon: int = 10) -> pd.Series:
    """
    Forecast conditional volatility for given horizon.
    Returns variance series (convert to volatility by sqrt if needed).
    """
    forecast = model.forecast(horizon=horizon)
    # 注意：forecast.variance 是 DataFrame，取最后一行
    var = forecast.variance.iloc[-1]
    sigma = var.pow(0.5)
    sigma.name = f"forecast_vol_{horizon}d"
    return sigma