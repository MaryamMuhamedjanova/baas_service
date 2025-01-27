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
    def _create_params(pin):
        return {"pin": pin}

    return _create_params


# Фикстура для выполнения GET-запроса
@pytest.fixture
def service_response(token, request_params):
    def _get_response(pin):
        params = request_params(pin)
        response = baas_request.service_clientsFull_get(params, token)
        return params, response

    return _get_response


# Универсальная функция проверки полей
def validate_fields(obj, expected_fields, obj_name):
    missing_fields = expected_fields - set(obj.keys())
    assert not missing_fields, f"Отсутствуют поля в {obj_name}: {missing_fields}"

    extra_fields = set(obj.keys()) - expected_fields
    assert not extra_fields, f"Обнаружены лишние поля в {obj_name}: {extra_fields}"


@allure.suite("(/api/clients/full) Получение полной информации по клиенту")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("pin", ["12006200000711"], ids=["12006200000711"])
    @allure.title("Поиск по корректному ИНН клиента")
    @allure.description("Этот тест проверяет успешный запрос по ИНН клиента")
    def test_get_list_account_clientCode_get_success_response(self, pin, service_response):
        # Выполнение запроса
        params, payment_response = service_response(pin)

        with allure.step("Проверка отправленных параметров запроса"):
            allure.attach("Request Parameters", urlencode(params), allure.attachment_type.TEXT)

        with allure.step("Логирование полного ответа"):
            print("Response status:", payment_response.status_code)
            print("Response body:", payment_response.text)

        with allure.step("Проверка тела ответа"):
            allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
            response_data = json.loads(payment_response.text)

            # Проверка верхнего уровня ответа
            validate_fields(response_data, {"data", "code", "message"}, "ответе")
            assert response_data["code"] == 0, f"Неожиданный код ответа: {response_data['code']}"
            assert response_data["message"] == "Success", f"Неожиданное сообщение: {response_data['message']}"

            # Проверка объекта 'data'
            client_data = response_data["data"]
            expected_fields_data = {
                "pin", "clientCode", "firstName", "isSalaryProject", "surname", "patronymic", "depId", "ordId",
                "nation", "fullName", "latSurName", "latName", "latFatherName", "residentialAddress", "birthAddress",
                "placeOfResidenceGrs", "dateOfBirth", "citizenStatus", "citizenship", "typeCode",
                "bankIdentificationLevel", "bankIdentifier", "isInArchive", "isInBlackList", "isBankClient",
                "clientFl", "passportDetails", "occupation", "contactInformation", "roles"
            }
            validate_fields(client_data, expected_fields_data, "'data' объекта")

            # Проверка вложенного объекта 'passportDetails'
            assert isinstance(client_data["passportDetails"], dict), "Поле 'passportDetails' должно быть объектом"
            expected_fields_passport = {"number", "series", "issuedBy", "issueDate", "dueDate", "nord"}
            validate_fields(client_data["passportDetails"], expected_fields_passport, "'passportDetails'")

            # Проверка вложенного объекта 'occupation'
            assert isinstance(client_data["occupation"], dict), "Поле 'occupation' должно быть объектом"
            expected_fields_occupation = {"title", "description"}
            validate_fields(client_data["occupation"], expected_fields_occupation, "'occupation'")

            # Проверка массива 'contactInformation'
            assert isinstance(client_data["contactInformation"], list), "Поле 'contactInformation' должно быть списком"
            for contact in client_data["contactInformation"]:
                assert isinstance(contact, dict), "Каждый элемент в 'contactInformation' должен быть объектом"
                validate_fields(contact, {"type", "value"}, "элементе 'contactInformation'")

            # Проверка массива 'roles'
            assert isinstance(client_data["roles"], list), "Поле 'roles' должно быть списком"
            for role in client_data["roles"]:
                assert isinstance(role, str), "Каждый элемент в 'roles' должен быть строкой"

            # Проверка конкретных типов полей
            assert isinstance(client_data["pin"], str), "Поле 'pin' должно быть строкой"
            assert isinstance(client_data["clientCode"], str), "Поле 'clientCode' должно быть строкой"
            assert isinstance(client_data["firstName"], str), "Поле 'firstName' должно быть строкой"
            assert isinstance(client_data["isSalaryProject"], bool), "Поле 'isSalaryProject' должно быть булевым"
            assert isinstance(client_data["dateOfBirth"], str), "Поле 'dateOfBirth' должно быть строкой (ISO 8601)"

        assert payment_response.status_code == 200, "Код ответа должен быть 200"
