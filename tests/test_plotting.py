import sys, os
from pathlib import Path

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC_DIR)

import pandas as pd
import numpy as np
from btcvol.plotting import plot_volatility, plot_compare, plot_scatter


def test_plot_functions(tmp_path: Path):
    # 生成模拟数据
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    s1 = pd.Series(np.random.randn(100).cumsum(), index=dates, name="BTC σ")
    s2 = pd.Series(np.random.randn(100).cumsum(), index=dates, name="ETH σ")

    # 输出目录（pytest 提供的临时路径）
    figdir = tmp_path / "figs"
    figdir.mkdir(parents=True, exist_ok=True)

    # 单资产波动率图
    out1 = figdir / "btc_vol.png"
    plot_volatility(s1, "BTC Volatility", outpath=str(out1))
    assert out1.exists()

    # 多资产比较图
    out2 = figdir / "compare_vol.png"
    plot_compare({"BTC": s1, "ETH": s2}, "BTC vs ETH Volatility", outpath=str(out2))
    assert out2.exists()

    # 散点图
    out3 = figdir / "scatter.png"
    plot_scatter(s1, s2, "BTC vs ETH Scatter", outpath=str(out3))
    assert out3.exists()