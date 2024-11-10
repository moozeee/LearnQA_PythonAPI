import json

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Куки с названием {cookie_name} в куках ответа на запрос не обнаружено"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Заголовка с названием {headers_name} в заголовках ответа на запрос не обнаружено"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Ответ сервера пришел не в JSON формате. Текста ответа - {response.text}"
        assert name in response_as_dict, f"В JSON ответа нет параметра {name}"
        return response_as_dict[name]
