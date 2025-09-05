from __future__ import annotations
import argparse, os
from pathlib import Path
import pandas as pd

from .config import Config
from .data import load_prices, to_log_returns, load_returns_panel
from .models import fit_garch11
from .diagnostics import ljung_box_test, jarque_bera_test
from .plotting import plot_volatility, plot_compare, plot_scatter


def _ensure_dirs(cfg: Config):
    for d in (cfg.outdir, cfg.figures_dir, cfg.tables_dir, cfg.models_dir):
        Path(d).mkdir(parents=True, exist_ok=True)


import pickle

def run_one_ticker(ticker: str, cfg: Config, show: bool = False, dist: str | None = None):
    """
    Run GARCH(1,1) estimation for a single ticker.
    Saves volatility plots, parameter tables, diagnostics, and model object.
    """
    dist = dist or cfg.dist
    px = load_prices(ticker, cfg.start, cfg.end)
    r = to_log_returns(px)
    res = fit_garch11(r, dist=dist)

    # Conditional volatility
    sigma = res.conditional_volatility.rename(f"{ticker}_sigma")
    vol_path = f"{cfg.figures_dir}/{ticker}_garch11_{dist}_vol.png"
    plot_volatility(sigma, f"{ticker} GARCH(1,1) – {dist}", vol_path, show=show)

    # Parameters
    params_df = res.params.to_frame("estimate")
    params_df["std_err"] = res.std_err
    params_df = params_df.fillna("NA")
    params_df.to_csv(f"{cfg.tables_dir}/{ticker}_garch11_{dist}_params.csv")

    # Diagnostics
    lb = ljung_box_test(res.std_resid, lags=20)
    jb = jarque_bera_test(res.std_resid.rename(f"{ticker}_std_resid"))
    pd.concat([lb, jb], axis=1).to_csv(f"{cfg.tables_dir}/{ticker}_garch11_{dist}_diag.csv")

    # Summary text
    with open(f"{cfg.tables_dir}/{ticker}_garch11_{dist}_summary.txt", "w") as f:
        f.write(res.summary().as_text())

    # Volatility series
    sigma.to_csv(f"{cfg.tables_dir}/{ticker}_garch11_{dist}_vol_series.csv")

    # Save model object (pickle)
    model_path = f"{cfg.models_dir}/{ticker}_garch11_{dist}_result.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(res, f)

    return r, sigma, params_df


def main():
    ap = argparse.ArgumentParser(description="BTC/ETH GARCH(1,1) runner")
    ap.add_argument("--start", default=Config.start)
    ap.add_argument("--end", default=Config.end)
    ap.add_argument("--tickers", nargs="+", default=list(Config.tickers))
    ap.add_argument("--dist", default=Config.dist, choices=["normal", "t", "skewt"])
    ap.add_argument("--outdir", default=Config.outdir)
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    cfg = Config(
    start=args.start, 
    end=args.end,
    tickers=tuple(args.tickers),
    dist=args.dist,
    outdir=args.outdir,
)

    sigmas = {}
    params_all = []
    for tk in cfg.tickers:
        r, sigma, params_df = run_one_ticker(tk, cfg, show=args.show, dist=cfg.dist)
        sigmas[tk] = sigma
        params_df.insert(0, "ticker", tk)
        params_all.append(params_df.reset_index().rename(columns={"index": "param"}))

    # Multi-ticker comparison
    if len(cfg.tickers) >= 2:
        series_map = {tk: s for tk, s in sigmas.items()}
        out = f"{cfg.figures_dir}/{'_'.join(cfg.tickers)}_garch11_{cfg.dist}_vol_compare.png"
        plot_compare(series_map, f"{' vs '.join(cfg.tickers)} Conditional Volatility – {cfg.dist}", out, show=args.show)

        sigma_df = pd.concat(series_map, axis=1).dropna()
        if isinstance(sigma_df.columns, pd.MultiIndex):
            sigma_df.columns = sigma_df.columns.droplevel(1)
        sigma_df.columns = [f"{c}_sigma" for c in sigma_df.columns]

        sigma_corr = sigma_df.corr()
        sigma_df.to_csv(f"{cfg.tables_dir}/vol_series_aligned.csv")
        sigma_corr.to_csv(f"{cfg.tables_dir}/vol_corr_matrix.csv")

        # Scatter plot of volatilities
        first, second = list(series_map.keys())[:2]
        x = sigma_df[f"{first}_sigma"].rename(f"{first} σ")
        y = sigma_df[f"{second}_sigma"].rename(f"{second} σ")
        plot_scatter(
            x, y,
            f"Volatility Scatter: {first} vs {second} – {cfg.dist}",
            f"{cfg.figures_dir}/{first}_vs_{second}_garch11_{cfg.dist}_vol_scatter.png",
            show=args.show
        )

        # Parameter summary across tickers
        params_summary = pd.concat(params_all, ignore_index=True)
        params_wide = params_summary.pivot(index="param", columns="ticker", values="estimate")
        params_wide.to_csv(f"{cfg.tables_dir}/garch11_{cfg.dist}_params_summary.csv")

        # Return panel descriptive stats
        ret_panel = load_returns_panel(list(cfg.tickers), cfg.start, cfg.end)
        desc = ret_panel.agg(["mean","std","skew","kurt"]).T
        desc.to_csv(f"{cfg.tables_dir}/returns_descriptive_stats.csv")
        ret_panel.corr().to_csv(f"{cfg.tables_dir}/returns_corr_matrix.csv")


if __name__ == "__main__":
    main()