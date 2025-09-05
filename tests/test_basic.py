import sys, os
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC_DIR)

import pytest
from btcvol.data import load_prices, to_log_returns
from btcvol.models import fit_garch11


def test_garch_minimal():
    px = load_prices("BTC-USD", "2024-01-01", "2024-06-30")
    assert not px.empty, "Price series is empty"
    assert px.name == "BTC-USD"

    r = to_log_returns(px)
    assert r.size > 50, "Too few return observations"

    res = fit_garch11(r, dist="t")

    # 参数存在性检查
    for k in ["omega", "alpha[1]", "beta[1]"]:
        assert k in res.params.index

    # 不再检查 res.converged / res.successful / res.optimizer
    # arch 的结果对象没有这些属性
    assert res.params.notna().all(), "Some parameters are NaN"