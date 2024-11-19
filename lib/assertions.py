from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict: dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате, Текст ответа - '{response.text}'"

        assert name in response_as_dict, f"В JSON ответе нет параметра {name}"
        assert str(response_as_dict[name]) == str(expected_value), error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict: dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате, Текст ответа - '{response.text}'"

        assert name in response_as_dict, f"В JSON ответе нет параметра {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict: dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате, Текст ответа - '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"В JSON ответе нет параметра {name}"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict: dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате, Текст ответа - '{response.text}'"
        for name in names:
            assert name not in response_as_dict, f"В JSON не должно быть параметра {name}"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == int(expected_status_code), \
            f"Код ответа сервера не соответствует ожидаемому. Текущий код ответа - {response.status_code}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict: dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате, Текст ответа - '{response.text}'"

        assert name not in response_as_dict, f"В JSON ответе есть параметр {name}, хотя его и не должно там быть"


