import allure
import pytest
import json
import data
import baas_request
from auth_token import generate_auth_token  # Импортируем функцию для получения токена


# Функция для формирования тела запроса
def get_CardList_body(clientCode):
    current_body = data.CardList_body.copy()
    current_body["clientCode"] = clientCode
    return current_body


# Позитивная проверка для получения списка карт клиента
def positive_assert_customerId(clientCode, token):
    service_CardList_body = get_CardList_body(clientCode)

    # Отправляем запрос с токеном
    payment_response = baas_request.service_CardList_post(service_CardList_body, token)

    with allure.step("Проверка отправленного запроса"):
        allure.attach("Request", str(service_CardList_body), allure.attachment_type.JSON)
    with allure.step("Проверка тела ответа"):
        allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
        response_data = json.loads(payment_response.text)
    print("Ответ от сервера:", response_data)  # Выводим весь ответ

    # Проверки
    assert payment_response.status_code == 200  # Проверка статуса ответа
    assert response_data.get(
         "message") == "Success", "Ответ не содержит ожидаемого сообщения"


# Тест-кейс для получения списка карт клиента
@allure.suite("(CardList) Получение списка карт клиента")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("clientCode", ["008.119115"], ids=["008.119115"])
    @allure.title("Поиск по корректному коду клиента: ")
    @allure.description("Этот тест проверяет успешный запрос по коду клиента")
    def test_get_list_account_clientCode_get_success_response(self, clientCode):
        token = generate_auth_token()  # Получаем токен
        positive_assert_customerId(clientCode, token)  # Передаем токен в функцию
