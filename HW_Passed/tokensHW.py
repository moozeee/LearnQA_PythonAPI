import json
import time

import requests

base_res = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

parsedJson = json.loads(base_res.text)
token = parsedJson['token']
timer = parsedJson['seconds']
print("Задача создана, Токен - ", token, "Таймер - ", timer)

get_params = {"token": {token}}
"""Отправляем запрос до завершения таймера"""
res = requests.get("https://playground.learnqa.ru/api/longtime_job", params=get_params)
if res.text.__contains__("NOT ready"):
    print("Ответ сервера до ожидания ", res.text)

"""Ждем пока кончится таймер задачи"""
print("Ждем ", timer, " секунд")
time.sleep(timer)

"""Отправляем запрос после завершения таймера"""
res = requests.get("https://playground.learnqa.ru/api/longtime_job", params=get_params)
if res.text.__contains__("Job is ready"):
    print("Ответ сервера после ожидания ", res.text)

