import re

from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    @allure.title("Test edit new user")
    @allure.description("Тест для проверки изменения нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):
        #Register
        register_data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                       first_name='learnqa', last_name='learnqa')
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        #Login
        login_data = {
            "email": email,
            "password": password,
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name},
        )

        Assertions.assert_status_code(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Неверное имя после изменения имени")

    @allure.title("Test edit a user w/o login")
    @allure.description("Тест для проверки изменения нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_wo_login(self):
        # Edit
        new_name = "Changed Name"

        response1 = MyRequests.put(
            f"/user/2",
            data={"firstName": new_name},
        )
        Assertions.assert_status_code(response1, 400)

    @allure.title("Test edit a user by user")
    @allure.description("Тест для проверки изменения нового пользователя под другим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_by_other_user(self):
        #Register new user 1
        register_data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                       first_name='learnqa', last_name='learnqa')
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        #Login by user 2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        #Edit user 1 by user 2
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name},
        )

        Assertions.assert_status_code(response3, 400)

    @allure.title("Test edit a users email to wrong one")
    @allure.description("Тест для проверки изменения емейла нового пользователя на невалидный")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_email_of_just_created_user_to_wrong(self):
        #Register
        register_data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                       first_name='learnqa', last_name='learnqa')
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        #Login
        login_data = {
            "email": email,
            "password": password,
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_email = re.sub('@', '', email)

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email},
        )

        Assertions.assert_status_code(response3, 400)

    @allure.title("Test edit a users name to wrong one")
    @allure.description("Тест для проверки изменения имени пользователя на короткое недопустимое")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_firstname_of_just_created_user_to_wrong(self):
        #Register
        register_data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                                       first_name='learnqa', last_name='learnqa')
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        #Login
        login_data = {
            "email": email,
            "password": password,
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_short_firstname = "f"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstname": new_short_firstname},
        )

        Assertions.assert_status_code(response3, 400)
