"""Rupee Tracker: a PKR remittance calculator using live exchange rates."""
import argparse
import json
import sys
import time
from pathlib import Path

import requests


API_URL = "https://open.er-api.com/v6/latest/{base}"
CACHE_FILE = Path(".rates_cache.json")
CACHE_TTL_SECONDS = 3600  # the API only updates daily; be gentle
CURRENCIES = ["USD", "AED", "SAR"]
ATTRIBUTION = "Rates by Exchange Rate API (https://www.exchangerate-api.com)"


def fetch_rates(base="PKR"):
    """Return the API response for `base`, using a local cache if fresh."""
    if CACHE_FILE.exists():
        try:
            cached = json.loads(CACHE_FILE.read_text())
            fresh = time.time() - cached["fetched_at"] < CACHE_TTL_SECONDS
            if cached["data"]["base_code"] == base and fresh:
                return cached["data"]
        except (json.JSONDecodeError, KeyError):
            pass  # bad cache file, just refetch

    response = requests.get(API_URL.format(base=base), timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("result") != "success":
        raise RuntimeError(f"API error: {data.get('error-type', 'unknown')}")

    CACHE_FILE.write_text(json.dumps({"fetched_at": time.time(), "data": data}))
    return data


def convert(amount, from_code, to_code, rates):
    """Convert using PKR-based rates (rates[X] = X per 1 PKR)."""
    return amount / rates[from_code] * rates[to_code]


def show_rates(data):
    rates = data["rates"]
    print(f"Live rates (updated {data['time_last_update_utc']})\n")
    print(f"{'Currency':<10}{'1 unit = PKR':>15}{'1 PKR =':>15}")
    for code in CURRENCIES:
        print(f"{code:<10}{1 / rates[code]:>15,.2f}{rates[code]:>15.5f}")


def show_conversion(amount, from_code, to_code, fee_percent, data):
    rates = data["rates"]
    fee = amount * fee_percent / 100
    result = convert(amount - fee, from_code, to_code, rates)
    print(f"Amount:    {amount:,.2f} {from_code}")
    if fee_percent:
        print(f"Fee ({fee_percent}%): {fee:,.2f} {from_code}")
    print(f"Receives:  {result:,.2f} {to_code}")
    print(f"Rate used: 1 {from_code} = {convert(1, from_code, to_code, rates):,.4f} {to_code}")


def build_parser():
    parser = argparse.ArgumentParser(description="PKR remittance calculator")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("rates", help="show PKR against USD, AED and SAR")

    conv = sub.add_parser("convert", help="convert an amount")
    conv.add_argument("amount", type=float)
    conv.add_argument("from_code", type=str.upper, choices=["PKR"] + CURRENCIES)
    conv.add_argument("to_code", type=str.upper, choices=["PKR"] + CURRENCIES)
    conv.add_argument("--fee", type=float, default=0.0,
                      help="transfer fee in percent, e.g. 1.5")
    return parser


def main():
    args = build_parser().parse_args()
    try:
        data = fetch_rates("PKR")
    except requests.RequestException as err:
        sys.exit(f"Could not reach the exchange rate API: {err}")
    except RuntimeError as err:
        sys.exit(str(err))

    if args.command == "rates":
        show_rates(data)
    else:
        show_conversion(args.amount, args.from_code, args.to_code, args.fee, data)
    print(f"\n{ATTRIBUTION}")


if __name__ == "__main__":
    main()