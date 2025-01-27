import allure
import pytest
import json
import baas_request
from auth_token import generate_auth_token

def positive_assert_customerId(clientCode, token):
    query_params = {"clientCode": clientCode}
    payment_response = baas_request.service_deposits_get(query_params, token)

    with allure.step("Проверка отправленного запроса"):
        allure.attach("Query Parameters", str(query_params), allure.attachment_type.JSON)

    with allure.step("Проверка тела ответа"):
        allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
        response_data = json.loads(payment_response.text)

    # print("Ответ от сервера:", response_data)

    assert payment_response.status_code == 200, "HTTP-статус не равен 200"
    assert response_data.get("message") == "Success", "Ответ не содержит ожидаемого сообщения"


@allure.suite("(Deposits) Получение списка депозитов клиента")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("clientCode", ["008.119115"], ids=["008.119115"])
    @allure.title("Поиск по корректному коду клиента: ")
    @allure.description("Этот тест проверяет успешный запрос по коду клиента")
    def test_get_list_account_clientCode_get_success_response(self, clientCode):
        token = generate_auth_token()
        positive_assert_customerId(clientCode, token)
