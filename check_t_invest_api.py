import os
import sys

print("=" * 60)
print("T-INVEST API CONNECTION TEST")
print("=" * 60)
print()

# Получение токена из переменной окружения
token = os.getenv("T_INVEST_TOKEN")

auth_status = "ERROR"
api_status = "ERROR"

if not token:
    print("Authentication: ERROR (T_INVEST_TOKEN not found)")
    print("API connection: ERROR")
else:
    try:
        from t_tech.invest import Client
        
        # Создаем клиент и выполняем простой запрос для проверки авторизации
        client = Client(token)
        
        try:
            # Простой запрос - получаем список счетов
            accounts_response = client.users.get_accounts()
            
            if accounts_response.accounts:
                auth_status = "OK"
                api_status = "OK"
            else:
                auth_status = "OK"  # Авторизация прошла, но нет счетов
                api_status = "OK"
        except Exception as e:
            error_msg = str(e)
            # Не выводим токен в ошибке
            if token in error_msg:
                error_msg = error_msg.replace(token, "***REDACTED***")
            print(f"Error during API call: {error_msg}")
            auth_status = "ERROR"
            api_status = "ERROR"
        finally:
            client.close()
        
    except ImportError as e:
        print(f"Import error: {e}")
        auth_status = "ERROR"
        api_status = "ERROR"
    except Exception as e:
        error_msg = str(e)
        if token and token in error_msg:
            error_msg = error_msg.replace(token, "***REDACTED***")
        print(f"Error: {error_msg}")
        auth_status = "ERROR"
        api_status = "ERROR"

print()
print(f"Authentication: {auth_status}")
print(f"API connection: {api_status}")
print()
print("=" * 60)
