# Rupee Tracker

A command-line PKR remittance calculator. It fetches **live exchange rates** from the [ExchangeRate-API](https://www.exchangerate-api.com/docs/free) open access endpoint (no API key needed) and lets you:

- See today's PKR rates against USD, AED and SAR
- Convert between PKR and USD, AED or SAR in either direction
- Subtract a transfer fee (in percent) to see what the receiver actually gets

Rates are cached locally for one hour, because the API only updates once a day and rate-limits heavy use.

## Requirements

- Python 3.9+
- The `requests` library

## Installation

```bash
git clone https://github.com/MuhammadTayyab789/RupeeTracker-PSEBAI.git
cd RupeeTracker-PSEBAI
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

If you use [uv](https://docs.astral.sh/uv/) instead:

```bash
uv sync
```

## Usage

Show current rates:

```bash
python rupee_tracker.py rates
```

Convert an amount:

```bash
python rupee_tracker.py convert 500 USD PKR
```

Convert with a transfer fee of 1.5%:

```bash
python rupee_tracker.py convert 50000 PKR SAR --fee 1.5
```

See all options:

```bash
python rupee_tracker.py --help
```

Supported currencies: `PKR`, `USD`, `AED`, `SAR`.

## Sample output

`python rupee_tracker.py rates`

```
PASTE YOUR REAL OUTPUT HERE
```

`python rupee_tracker.py convert 50000 PKR SAR --fee 1.5`

```
PASTE YOUR REAL OUTPUT HERE
```

## How it works

1. `fetch_rates()` calls `https://open.er-api.com/v6/latest/PKR` with `requests` and checks that the API reports success.
2. The response is cached in `.rates_cache.json` (ignored by git) for one hour.
3. `convert()` uses the PKR-based rates to convert between any two supported currencies.

## Project structure

```
rupee_tracker.py    main program
requirements.txt    dependencies
.gitignore          ignores .venv/, __pycache__/, .env
README.md           this file
```

## Attribution

Rates by [Exchange Rate API](https://www.exchangerate-api.com).# RupeeTracker-PSEBAI
