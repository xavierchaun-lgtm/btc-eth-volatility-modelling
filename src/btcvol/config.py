from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Config:
    start: str = "2018-01-01"
    end: str   = "2024-12-31"
    tickers: tuple[str, ...] = ("BTC-USD", "ETH-USD")
    dist: str = "t"
    outdir: str = "results"

    figures_dir: str = field(init=False)
    tables_dir: str = field(init=False)
    models_dir: str = field(init=False)

    def __post_init__(self):
        out = Path(self.outdir)
        self.figures_dir = str(out / "figures")
        self.tables_dir = str(out / "tables")
        self.models_dir = str(out / "models")