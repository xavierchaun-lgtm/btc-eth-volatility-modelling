# BTC vs ETH Volatility Modelling (GARCH)

This project compares the volatility of **Bitcoin (BTC)** and **Ethereum (ETH)** using **GARCH(1,1)** models with different innovation distributions (`normal`, `t`, `skewt`).

The codebase is modular, fully tested with `pytest`, and includes both **CLI tools** and **Jupyter notebooks** for reproducibility.

---

## 📂 Project Structure
btc-eth-volatility-modelling/
├── src/btcvol/           # Core package
│   ├── __init__.py
│   ├── config.py         # Config dataclass
│   ├── data.py           # Data loading & returns
│   ├── models.py         # GARCH(1,1) fitting
│   ├── diagnostics.py    # Ljung-Box, Jarque-Bera tests
│   ├── plotting.py       # Volatility & scatter plots
│   └── cli.py            # Command-line interface
├── notebooks/            # Jupyter notebooks (demos)
│   └── btc_eth_demo.ipynb
├── tests/                # Unit tests
│   ├── test_basic.py
│   └── test_plotting.py
├── results/              # Auto-generated results:
│   ├── figures/          # All generated plots and figures
│   ├── tables/           # Summary tables (e.g., parameter tables, diagnostics)
│   ├── models/           # Saved model summaries
│   └── forecast/         # Forecast CSVs for future volatility predictions
├── requirements.txt
└── README.md
---

## ⚙️ Installation

```bash
# Clone repo
git clone https://github.com/xavierchaun-lgtm/btc-eth-volatility-modelling.git
cd btc-eth-volatility-modelling

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

▶️ Usage

1. Run via CLI

Run BTC & ETH comparison over 2020–2024 with Student-t innovations:
python -m src.btcvol.cli \
  --tickers BTC-USD ETH-USD \
  --start 2020-01-01 --end 2024-12-31 \
  --dist t \
  --outdir results \
  --show

  Outputs:
	•	Figures → results/figures/
	•	Tables → results/tables/
	•	Model summaries → results/models/

2. Run Jupyter Notebook

Open the demo notebook:
jupyter notebook notebooks/btc_eth_demo.ipynb

3. Run Tests

All core functionality is tested with pytest.

pytest -q

Expected output:
..                                                                                                                                            [100%]
2 passed in 2.89s

4. Run Forecast Script

Run the forecast script to generate future volatility predictions:
python tests/test_forecast.py

Outputs:
	•	Forecast CSV files → results/forecast/
	•	Forecast plots → results/figures/

📊 Example Outputs
	•	Volatility Comparison: BTC vs ETH conditional volatility curves
	•	Scatter Plot: BTC vs ETH volatility correlation
	•	Diagnostics: Ljung-Box & Jarque-Bera test results
	•	Parameter Tables: GARCH(1,1) parameter estimates with standard errors
	•	Forecast Results: BTC/ETH 未来波动率预测（CSV 文件位于 results/forecast/，图表位于 results/figures/）

⸻

📚 References
	•	Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity. Journal of Econometrics.
	•	Engle, R. (1982). Autoregressive Conditional Heteroskedasticity with Estimates of the Variance of UK Inflation. Econometrica.

⸻

🧪 Status

✅ Stable — tested with pytest and ready for experimentation.