import pytest
import requests

def generate_auth_token():
    url = "http://baas-test.hbk.kg/api/system/authorization/login"
    auth_body = {
        "login": "cWE=",
        "password": "cGFzc3dvcmQxMjM="
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=auth_body, headers=headers)
    print("Код состояния:", response.status_code)
    print("Ответ сервера:", response.text)
    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("data", {}).get("token")
        if token:
            print("Токен успешно получен:", token)
            return token
        else:
            raise ValueError("Не удалось извлечь токен из ответа.")
    else:
        raise ValueError(f"Ошибка получения токена: {response.status_code}, {response.text}")


