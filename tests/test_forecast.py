import sys, os
import pandas as pd
import matplotlib.pyplot as plt

# 把 src 加到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from btcvol.models import load_model, forecast_volatility


def run_forecast(tickers, horizon=10, dist="t"):
    results = {}

    # 确保 forecast 目录存在
    os.makedirs("results/forecast", exist_ok=True)

    for tk in tickers:
        model_path = f"results/models/{tk}_garch11_{dist}_result.pkl"
        if not os.path.exists(model_path):
            print(f"[WARN] Model file not found: {model_path}")
            continue

        print(f"\n=== Loading model for {tk} ===")
        model = load_model(model_path)

        print("\n--- Parameters ---")
        print(model.params)

        sigma_forecast = forecast_volatility(model, horizon=horizon)
        print(f"\n--- {tk} Forecast Volatility ({horizon} days) ---")
        print(sigma_forecast)

        # 保存 CSV 到 results/forecast/
        outpath = f"results/forecast/forecast_{tk}.csv"
        sigma_forecast.to_csv(outpath)
        print(f"[OK] Saved forecast to {outpath}")

        results[tk] = sigma_forecast

    # 如果有多个资产 → 合并对比并画图
    if len(results) > 1:
        df = pd.concat(results, axis=1)
        outpath = "results/forecast/forecast_compare.csv"
        df.to_csv(outpath)
        print(f"[OK] Saved multi-asset forecast comparison to {outpath}")

        # 画图（依然保存到 figures/）
        ax = df.plot(marker="o")
        ax.set_title(f"GARCH(1,1) Forecast Volatility ({horizon} days)")
        ax.set_ylabel("Volatility (%)")
        ax.set_xlabel("Forecast Horizon")
        ax.legend(title="Ticker")
        fig = ax.get_figure()
        fig.savefig("results/figures/forecast_compare.png", bbox_inches="tight", dpi=220)
        plt.close(fig)
        print("[OK] Saved forecast plot to results/figures/forecast_compare.png")


if __name__ == "__main__":
    # 默认跑 BTC + ETH
    run_forecast(["BTC-USD", "ETH-USD"], horizon=10, dist="t")