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
        assert response_as_dict[name] == expected_value, error_message