import requests
import pytest


class TestCookieAssert:

    def test_cookie_assert(self):
        res = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        if res.status_code == 200 and len(res.cookies) > 0:
            for cookie in res.cookies:
                if cookie.name == "HomeWork":
                    assert cookie.name == "HomeWork", f"Куки c именем 'HomeWork' не была найдена в куках ответа. Что-то пошло не так"
                    assert cookie.value == "hw_value", f"Значение куки 'HomeWork' не равно 'hw_value'. Что-то пошло не так"
                print("\r\n", cookie.name, "=", cookie.value)

    def test_headers_assert(self):
        res = requests.get("https://playground.learnqa.ru/api/homework_header")
        if res.status_code == 200 and len(res.headers) > 0:
            if "x-secret-homework-header" in res.headers:
                header = res.headers["x-secret-homework-header"]
                assert header == "Some secret value", f"Значение заголовка 'x-secret-homework-header' не равно 'Some secret value'. Что-то пошло не так"
                print("\r\n", header)
