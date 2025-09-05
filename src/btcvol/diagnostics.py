from __future__ import annotations
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera


def ljung_box_test(residuals: pd.Series, lags: int = 20) -> pd.DataFrame:
    """
    Ljung-Box test for autocorrelation in residuals.
    """
    lb = acorr_ljungbox(residuals, lags=[lags], return_df=True)
    lb.index = [residuals.name if residuals.name else f"LjungBox_lags{lags}"]
    return lb


def jarque_bera_test(series: pd.Series) -> pd.DataFrame:
    """
    Jarque-Bera test for normality.
    """
    stat, p, skew, kurt = jarque_bera(series)
    return pd.DataFrame(
        {"JB_stat": [stat], "p_value": [p], "skew": [skew], "kurtosis": [kurt]},
        index=[series.name if series.name else "series"]
    )