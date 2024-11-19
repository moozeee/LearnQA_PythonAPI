from datetime import datetime

import allure

from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    @allure.title("Test get user no login")
    @allure.description("Тест для проверки получения данных пользователя без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%Y%m%d%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    @allure.title("Test get user")
    @allure.description("Тест для проверки получения данных пользователя c авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid}
                                   )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Test get user by other user")
    @allure.description("Тест для проверки получения данных пользователя c авторизацией под другим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_different_user(self):
        data = {
            "email": 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        other_user_id = self.get_json_value(response1, "user_id") + 1

        response2 = MyRequests.get(f"/user/{other_user_id}",
                                   headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid}
                                   )
        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, expected_fields)
