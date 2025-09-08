# BTC vs ETH Volatility Modelling (GARCH)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/xavierchaun-lgtm/btc-eth-volatility-modelling)

📈 This project compares the volatility of **Bitcoin (BTC)** and **Ethereum (ETH)**  
using **GARCH(1,1)** models. It supports data fetching via `yfinance`, volatility estimation with `arch`,  
and provides visualization + forecast results.

---

## 📚 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Example Outputs](#-example-outputs)
- [License](#-license)

---

## 🚀 Features
- Download BTC/ETH prices automatically from Yahoo Finance
- Fit GARCH(1,1) models with normal, t, or skew-t distribution
- Save parameter tables, diagnostics, and volatility plots
- Forecast future volatility and compare BTC vs ETH

---

## ⚙️ Installation
```bash
git clone https://github.com/xavierchaun-lgtm/btc-eth-volatility-modelling.git
cd btc-eth-volatility-modelling
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

▶️ Usage

Run CLI
python -m src.btcvol.cli --tickers BTC-USD ETH-USD --start 2023-01-01 --end 2023-06-30 --dist t --outdir results

Run Forecast Script
python tests/test_forecast.py
Outputs will be saved in:
	•	Results CSVs → results/forecast/
	•	Figures → results/figures/

  btc-eth-volatility-modelling/
├── notebooks/              # Jupyter notebooks for demo/experiments
├── src/btcvol/             # Core package
│   ├── __init__.py
│   ├── cli.py              # Command line interface
│   ├── config.py           # Config dataclass
│   ├── data.py             # Data loading (yfinance)
│   ├── diagnostics.py      # Ljung-Box, JB test
│   ├── models.py           # Fit GARCH(1,1), save/load models
│   └── plotting.py         # Visualization helpers
├── tests/                  # Test scripts
│   ├── test_basic.py
│   ├── test_forecast.py
│   └── test_plotting.py
├── results/                # Generated outputs (ignored by git)
│   ├── figures/
│   ├── tables/
│   ├── models/
│   └── forecast/
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
🚀 Usage

CLI: Run full pipeline
python -m src.btcvol.cli --tickers BTC-USD ETH-USD \
  --start 2023-01-01 --end 2023-06-30 \
  --dist t --outdir results

Manual test script:
python tests/test_forecast.py
Outputs will be saved in:
	•	Results CSVs → results/forecast/
	•	Figures → results/figures/

📊 Example Outputs

Conditional Volatility (BTC vs ETH)
Forecasted Volatility (10 days)

🤝 Contributing
Feel free to fork this repo, open pull requests or raise issues.
You can suggest new features (e.g., EGARCH, GJR-GARCH, DCC models), or help improve CLI interfaces or plotting style.


📜 License
This project is licensed under the MIT License.
You are free to use, copy, modify, and distribute this software for personal or commercial use.

👨‍💻 Author
Xiaochuan Li
GitHub: @xavierchaun-lgtm
Email: xiaochuanformal@gmail.com
