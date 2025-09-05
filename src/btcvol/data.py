from __future__ import annotations
import pandas as pd
import numpy as np
import yfinance as yf

def load_prices(ticker: str, start: str, end: str) -> pd.Series:
    """
    Download adjusted close prices for a given ticker and date range.
    Always return a single-column Series named as `ticker`.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned by yfinance for {ticker} in [{start}, {end}]")

    # Case 1: 普通 DataFrame（列名是 "Close"）
    if "Close" in df.columns:
        px = df["Close"].copy()

    # Case 2: MultiIndex DataFrame（(ticker, "Close")）
    elif isinstance(df.columns, pd.MultiIndex):
        close_df = df.xs("Close", axis=1, level=-1)
        if ticker in close_df.columns:
            px = close_df[ticker].copy()
        else:
            px = close_df.iloc[:, 0].copy()
    else:
        raise KeyError("No 'Close' column found in yfinance data.")

    # 确保返回 Series
    if isinstance(px, pd.DataFrame) and px.shape[1] == 1:
        px = px.iloc[:, 0].copy()

    px.name = ticker
    px = px.sort_index()
    return px


def to_log_returns(price: pd.Series) -> pd.Series:
    """
    Convert price series to log returns (decimal).
    """
    price = price.ffill().dropna().astype(float)
    r = np.log(price).diff().dropna()
    r.name = f"{price.name}_logret"
    return r


def load_returns_panel(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Load log returns for multiple tickers and return as a DataFrame
    aligned on dates (inner join by default).
    """
    series = [to_log_returns(load_prices(tk, start, end)) for tk in tickers]
    df = pd.concat(series, axis=1).dropna(how="all")
    return df