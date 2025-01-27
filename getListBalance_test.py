import pytest
import allure
import json
import data
import baas_request
from auth_token import generate_auth_token


# Фикстура для генерации токена
@pytest.fixture
def token():
    return generate_auth_token()


# Фикстура для подготовки тела запроса
@pytest.fixture
def request_body():
    def _create_body(clientCode):
        current_body = data.getListBalance_body.copy()
        current_body["clientCode"] = clientCode
        return current_body

    return _create_body


# Фикстура для выполнения запроса
@pytest.fixture
def service_response(token, request_body):
    def _get_response(clientCode):
        body = request_body(clientCode)
        response = baas_request.service_getListBalance_get(body, token)
        return body, response

    return _get_response


# Универсальная функция проверки полей
def validate_fields(obj, expected_fields, obj_name):
    missing_fields = expected_fields - set(obj.keys())
    assert not missing_fields, f"Отсутствуют поля в {obj_name}: {missing_fields}"

    extra_fields = set(obj.keys()) - expected_fields
    assert not extra_fields, f"Обнаружены лишние поля в {obj_name}: {extra_fields}"


# Тест с использованием фикстур
@allure.suite("(GetListBalance) Получение списка счетов клиента с балансами")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("clientCode", ["008.119115"], ids=["008.119115"])
    @allure.title("Поиск по корректному коду клиента: ")
    @allure.description("Этот тест проверяет успешный запрос по коду клиента")
    def test_get_list_account_clientCode_get_success_response(self, clientCode, service_response):
        body, payment_response = service_response(clientCode)

        with allure.step("Проверка отправленного запроса"):
            allure.attach("Request", str(body), allure.attachment_type.JSON)

        with allure.step("Проверка тела ответа"):
            allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
            response_data = json.loads(payment_response.text)

            validate_fields(response_data, {"data", "code", "message"}, "ответе")

            assert isinstance(response_data["data"], list), "Поле 'data' должно быть списком"
            assert response_data["code"] == 0, "Поле 'code' должно быть равно 0"
            assert response_data["message"] == "Success", "Поле 'message' должно быть равно 'Success'"

            for account in response_data["data"]:
                validate_fields(account,
                                {"number", "currency", "balance", "availableAmount", "blockedAmount"}, "записи")
                assert isinstance(account["balance"], (int, float)), "Поле 'balance' должно быть числом"
                assert isinstance(account["availableAmount"], (int, float)), "Поле 'availableAmount' должно быть числом"
                assert isinstance(account["blockedAmount"], (int, float)), "Поле 'blockedAmount' должно быть числом"

        assert payment_response.status_code == 200, "Код ответа должен быть 200"
