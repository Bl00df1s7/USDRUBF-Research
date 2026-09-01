#!/usr/bin/env python3
"""
Проверка подключения к T-Invest API и поиск инструмента USDRUBF.
"""

import os
import sys

from t_tech.invest import Client
from t_tech.invest.schemas import InstrumentStatus


def main():
    print("=" * 60)
    print("INSTRUMENT TEST")
    print("=" * 60)
    print()

    token = os.getenv("T_INVEST_TOKEN")
    if not token:
        print("Error: T_INVEST_TOKEN not found in environment variables")
        sys.exit(1)

    try:
        with Client(token=token) as client:
            # Получаем список всех фьючерсов
            response = client.instruments.futures(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)

            # Ищем USDRUBF по ticker
            target_ticker = "USDRUBF"
            found_instrument = None

            for instrument in response.instruments:
                if instrument.ticker == target_ticker:
                    found_instrument = instrument
                    break

            if found_instrument:
                print(f"Ticker: {found_instrument.ticker}")
                print(f"Name: {found_instrument.name}")
                print(f"UID: {found_instrument.uid}")
                print(f"FIGI: {found_instrument.figi}")
                
                # Получаем статус торговли
                trading_status_response = client.instruments.get_trading_status(figi=found_instrument.figi)
                status_map = {
                    0: "UNSPECIFIED",
                    1: "OPEN",
                    2: "CLOSED",
                    3: "BREAK",
                }
                trading_status = status_map.get(trading_status_response.trading_status, "UNKNOWN")
                print(f"Trading status: {trading_status}")
            else:
                print(f"Instrument with ticker '{target_ticker}' not found.")
                print()
                print("Nearest matches by ticker/name:")
                # Ищем похожие инструменты
                matches = []
                for instrument in response.instruments:
                    if "USD" in instrument.ticker.upper() or "RUB" in instrument.ticker.upper() or \
                       "USD" in instrument.name.upper() or "RUB" in instrument.name.upper():
                        matches.append(instrument)
                
                if matches:
                    for inst in matches[:10]:  # Показываем до 10 совпадений
                        print(f"  Ticker: {inst.ticker}, Name: {inst.name}, FIGI: {inst.figi}, UID: {inst.uid}")
                else:
                    print("  No matches found containing 'USD' or 'RUB'.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
