#!/usr/bin/env python3
"""Минимальный скрипт для проверки окружения T-Invest."""

import os

# 1. Проверка импорта SDK
try:
    import t_tech.invest
    sdk_status = "OK"
except ImportError:
    sdk_status = "ERROR"

# 2. Проверка наличия токена в переменной окружения
token = os.environ.get("T_INVEST_TOKEN")
if token:
    token_status = "FOUND"
else:
    token_status = "NOT FOUND"

# 3. Вывод результатов (не выводим сам токен)
print(f"T-Invest SDK: {sdk_status}")
print(f"T_INVEST_TOKEN: {token_status}")
