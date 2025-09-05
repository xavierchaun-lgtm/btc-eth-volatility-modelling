from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_volatility(sigma: pd.Series, title: str, outpath: str | None = None, show: bool = False):
    fig, ax = plt.subplots()
    sigma.plot(ax=ax, lw=1.2)
    ax.set_title(title)
    ax.set_ylabel("Conditional volatility (%)")
    ax.set_xlabel("")
    if outpath:
        Path(outpath).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(outpath, bbox_inches="tight", dpi=220)
    if show:
        plt.show()
    plt.close(fig)
    return fig, ax


def plot_compare(series_map: dict[str, pd.Series], title: str, outpath: str | None = None, show: bool = False):
    fig, ax = plt.subplots()
    for name, s in series_map.items():
        s.plot(ax=ax, lw=1.2, label=name)
    ax.set_title(title)
    ax.set_ylabel("Conditional volatility (%)")
    ax.set_xlabel("")
    ax.legend()
    if outpath:
        Path(outpath).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(outpath, bbox_inches="tight", dpi=220)
    if show:
        plt.show()
    plt.close(fig)
    return fig, ax


def plot_scatter(x: pd.Series, y: pd.Series, title: str, outpath: str | None = None, show: bool = False):
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=20, alpha=0.6, edgecolor="k", linewidth=0.2)
    ax.plot([x.min(), x.max()], [x.min(), x.max()], ls="--", c="red", lw=1)  # 对角线
    ax.set_title(title)
    ax.set_xlabel(f"{x.name}")
    ax.set_ylabel(f"{y.name}")
    if outpath:
        Path(outpath).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(outpath, bbox_inches="tight", dpi=220)
    if show:
        plt.show()
    plt.close(fig)
    return fig, ax