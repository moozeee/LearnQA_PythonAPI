import json
from datetime import datetime

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


    def prepare_registration_data(self, rand_email=False, email=None, username=None, password=None, first_name=None,
                                  last_name=None):
        return_data = {}
        if email is None:
            if rand_email:
                return_data["email"] = self.create_random_email()
        else:
            return_data["email"] = email
        if username is not None:
            return_data["username"] = username
        if password is not None:
            return_data["password"] = password
        if first_name is not None:
            return_data["firstName"] = first_name
        if last_name is not None:
            return_data["lastName"] = last_name

        return return_data

    def create_random_email(self, email="learnqa"):
        base_part = email
        domain = "example.com"
        random_part = datetime.now().strftime("%Y%m%d%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        return email
