import json

import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic('Authorization cases')
class TestUserDelete(BaseCase):

    def login_user(self, email=None, password=None):

        if email is None and password is None:
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        else:
            data = {
                'email': email,
                'password': password
            }

        response1 = MyRequests.post('/user/login', data=data)
        if response1.status_code == 200:
            self.auth_sid = self.get_cookie(response1, "auth_sid")
            self.token = self.get_header(response1, "x-csrf-token")
            self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.title("Test delete default user")
    @allure.description("Тест для проверки невозможности удаления дефолтного пользователя")
    def test_user_delete_id2(self):
        #Login
        self.login_user()
        response2 = MyRequests.get('/user/auth',
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "UserId из метода авторизации не равен UserId из метода проверки")

        #Delete try
        delete_response = MyRequests.delete('/user/2',
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid})
        Assertions.assert_status_code(delete_response, "400")

    @allure.title("Test delete new user")
    @allure.description("Тест для проверки удаления новоого пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_just_created_user(self):
        #Create user
        data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123', first_name='learnqa',
                                              last_name='learnqa')

        response = MyRequests.post("/user", data=data)
        user_id = self.get_json_value(response, "id")
        email = data['email']
        password = data['password']
        Assertions.assert_status_code(response, 200)

        #Login
        self.login_user(email=email, password=password)
        response2 = MyRequests.get('/user/auth',
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2, "user_id", user_id,
                                             "UserId из метода авторизации не равен UserId из метода проверки")

        #Delete try
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid})
        Assertions.assert_status_code(delete_response, "200")
        # Get
        response3 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_status_code(response3, "404")

    @allure.title("Test delete user by user")
    @allure.description("Тест для проверки удаления пользователя под другим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_user_by_other_user(self):
        # Create user to delete
        data = self.prepare_registration_data(rand_email=True, username='learnqa', password='123',
                                              first_name='learnqa',
                                              last_name='learnqa')

        response = MyRequests.post("/user", data=data)
        user_id = self.get_json_value(response, "id")
        email = data['email']
        password = data['password']
        Assertions.assert_status_code(response, 200)

        # Login as default user
        self.login_user()
        response2 = MyRequests.get('/user/auth',
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2, "user_id", 2,
                                             "UserId из метода авторизации не равен UserId из метода проверки")

        # Delete try
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid})
        Assertions.assert_status_code(delete_response, "400")

