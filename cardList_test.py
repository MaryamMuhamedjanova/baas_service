import allure
import pytest
import json
import data
import baas_request
from auth_token import generate_auth_token

def get_CardList_body(clientCode):
    current_body = data.CardList_body.copy()
    current_body["clientCode"] = clientCode
    return current_body


def positive_assert_customerId(clientCode, token):
    service_CardList_body = get_CardList_body(clientCode)

    payment_response = baas_request.service_CardList_post(service_CardList_body, token)

    with allure.step("Проверка отправленного запроса"):
        allure.attach("Request", str(service_CardList_body), allure.attachment_type.JSON)

    with allure.step("Проверка тела ответа"):
        allure.attach("Response", str(payment_response.text), allure.attachment_type.TEXT)
        response_data = json.loads(payment_response.text)

        expected_fields = {"data"}
        missing_fields = expected_fields - set(response_data.keys())
        assert not missing_fields, f"Отсутствуют поля в ответе: {missing_fields}"

        assert isinstance(response_data["data"], dict), "Поле 'data' должно быть объектом"
        data_expected_fields = {"accounts"}
        missing_data_fields = data_expected_fields - set(response_data["data"].keys())
        assert not missing_data_fields, f"Отсутствуют поля в 'data': {missing_data_fields}"

        assert isinstance(response_data["data"]["accounts"], list), "Поле 'accounts' должно быть списком"
        account_fields = {
            "cardNumber", "cardProductCode", "absAccount", "currency", "balance",
            "availAmount", "blockedAmount", "status", "statusActual", "holderName",
            "issueDate", "expireDate", "cardType", "cardId", "processing", "cardFl",
            "overdraft", "department", "isAdditional", "internetPayments", "defaultFL",
            "clientName", "processingClientId", "creditCardInfo", "limits",
            "organizationSalary", "virtualCard", "cardProductId", "casCardId",
            "productionId", "productionBranch", "productionStatus", "blockeason",
            "smsNotificationNumber", "notificationType"
        }

        for account in response_data["data"]["accounts"]:
            missing_account_fields = account_fields - set(account.keys())
            assert not missing_account_fields, f"Отсутствуют поля: {missing_account_fields}"

            extra_account_fields = set(account.keys()) - account_fields
            assert not extra_account_fields, f"Обнаружены лишние поля: {extra_account_fields}"

            assert "creditCardInfo" in account, "Отсутствует поле 'creditCardInfo' в account"
            credit_card_info_fields = {
                "creditLimit", "availableLimit", "interestRate", "minPaymAmnt",
                "paymDate", "unpaidMinPaymPrevMont"
            }
            credit_card_info = account["creditCardInfo"]
            assert isinstance(credit_card_info, dict), "Поле 'creditCardInfo' должно быть объектом"
            missing_credit_card_info_fields = credit_card_info_fields - set(credit_card_info.keys())
            assert not missing_credit_card_info_fields, f"Отсутствуют поля в 'creditCardInfo': {missing_credit_card_info_fields}"

            extra_credit_card_info_fields = set(credit_card_info.keys()) - credit_card_info_fields
            assert not extra_credit_card_info_fields, f"Обнаружены лишние поля в 'creditCardInfo': {extra_credit_card_info_fields}"

    # print("Ответ от сервера:", response_data)

    assert payment_response.status_code == 200
    assert response_data.get(
         "message") == "Success", "Ответ не содержит ожидаемого сообщения"


@allure.suite("(CardList) Получение списка карт клиента")
class TestSuite:
    @allure.sub_suite("Позитивные тест-кейсы")
    @pytest.mark.parametrize("clientCode", ["008.119115"], ids=["008.119115"])
    @allure.title("Поиск по корректному коду клиента: ")
    @allure.description("Этот тест проверяет успешный запрос по коду клиента")
    def test_get_list_account_clientCode_get_success_response(self, clientCode):
        token = generate_auth_token()
        positive_assert_customerId(clientCode, token)
