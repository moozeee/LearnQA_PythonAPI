from datetime import datetime

import allure

from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    exclude_params = [
        ("no_email"),
        ("no_username"),
        ("no_password"),
        ("no_firstname"),
        ("no_lastname"),
        ("too_short_name"),
        ("too_long_name")
    ]
    email = 'vinkotov@example.com'

    def test_create_user_successfully(self):
        data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123', first_name='learnqa',
                                              last_name='learnqa')

        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data(email=self.email, username='learnqa', password='123', first_name='learnqa',
                                              last_name='learnqa')

        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email 'vinkotov@example.com' already exists", f"Текст ответа некорректный. Текущий ответ {response.content}"

    @allure.description("Этот тест проверяет невозможность регистрации пользователя без @ d емейле")
    def test_negative_register_wo_at_check(self):
        email = 'emailwithoutatsymbol.com'
        data = self.prepare_registration_data(email=email, username='learnqa', password='123', first_name='learnqa',
                                              last_name='learnqa')
        response = MyRequests.post("/user", data=data)
        Assertions.assert_status_code(response, 400)

    @allure.description("Этот тест проверяет невозможность регистрации пользователя без каждого из параметров")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_register_without_params_check(self, condition):

        if condition == "no_email":
            data = self.prepare_registration_data(username='learnqa', password='123', first_name='learnqa',
                                                  last_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
        elif condition == "no_username":
            data = self.prepare_registration_data(rand_email=True, password='123', first_name='learnqa',
                                                  last_name='learnqa')
            response = MyRequests.post("/user", data=data)
        elif condition == "no_password":
            data = self.prepare_registration_data(rand_email=True, username='learnqa', first_name='learnqa',
                                                  last_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
        elif condition == "no_firstname":
            data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                  last_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
        elif condition == "no_lastname":
            data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                  first_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
        elif condition == "too_short_name":
            data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                  first_name='l', last_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
        elif condition == "too_long_name":
            data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                  first_name='Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ',
                                                  last_name='learnqa')
            response = MyRequests.post("/user", data=data)
            Assertions.assert_status_code(response, 400)
