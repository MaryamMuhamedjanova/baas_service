import pytest
import allure
import json
import data
import baas_request
from auth_token import generate_auth_token
from urllib.parse import urlencode


# Фикстура для генерации токена
@pytest.fixture
def token():
    return generate_auth_token()


# Фикстура для подготовки параметров запроса
@pytest.fixture
def request_params():
    def _create_params(accountNumber):
        return {"accountNumber": accountNumber}

    return _create_params


# Фикстура для выполнения GET-запроса
@pytest.fixture
def service_response(token, request_params):
    def _get_response(accountNumber):
        params = request_params(accountNumber)
        response = baas_request.service_Accounts_get(params, token)
        return params, response

    return _get_response


# Универсальная функция проверки полей
def validate_fields(obj, expected_fields, obj_name):
    missing_fields = expected_fields - set(obj.keys())
    assert not missing_fields, f"Отсутствуют поля в {obj_name}: {missing_fields}"

    extra_fields = set(obj.keys()) - expected_fields
    assert not extra_fields, f"Обнаружены лишние поля в {obj_name}: {extra_fields}"


@allure.suite("(Accounts) Получение информации по счёту")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("accountNumber", ["1250820004787445"], ids=["1250820004787445"])
    @allure.title("Поиск по корректному номеру счета")
    @allure.description("Этот тест проверяет успешный запрос по номеру счета")

    def test_get_list_account_clientCode_get_success_response(self, accountNumber, service_response):
        params, payment_response = service_response(accountNumber)

        with allure.step("Проверка отправленных параметров запроса"):
            allure.attach("Request Parameters", urlencode(params), allure.attachment_type.TEXT)

        # with allure.step("Логирование полного ответа"):
        #     print("Response status:", payment_response.status_code)
        #     print("Response body:", payment_response.text)

        with allure.step("Проверка тела ответа"):
            allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
            response_data = json.loads(payment_response.text)

            validate_fields(response_data, {"data", "code", "message"}, "ответе")

            assert isinstance(response_data["data"], dict), "Поле 'data' должно быть объектом"
            assert response_data["code"] == 0, "Поле 'code' должно быть равно 0"
            assert response_data["message"] == "Success", "Поле 'message' должно быть равно 'Success'"

            # Проверка полей внутри объекта 'data'
            account = response_data["data"]
            validate_fields(account,
                            {"number", "bic", "bank", "currency", "clientCode", "status", "type", "creationDate", "product", "balance"},
                            "записи")

            # Проверка объекта 'type'
            assert isinstance(account["type"], dict), "Поле 'type' должно быть объектом"
            validate_fields(account["type"], {"title"}, "'type'")

            # Проверка объекта 'product'
            assert isinstance(account["product"], dict), "Поле 'product' должно быть объектом"
            validate_fields(account["product"], {"title"}, "'product'")

            # Проверка объекта 'balance'
            assert isinstance(account["balance"], dict), "Поле 'balance' должно быть объектом"
            validate_fields(account["balance"], {"balance", "availableAmount", "blockedAmount"}, "'balance'")

            # Проверка числовых полей
            assert isinstance(account["balance"]["balance"], (int, float)), "Поле 'balance.balance' должно быть числом"
            assert isinstance(account["balance"]["availableAmount"], (int, float)), "Поле 'balance.availableAmount' должно быть числом"
            assert isinstance(account["balance"]["blockedAmount"], (int, float)), "Поле 'balance.blockedAmount' должно быть числом"

        assert payment_response.status_code == 200, "Код ответа должен быть 200"