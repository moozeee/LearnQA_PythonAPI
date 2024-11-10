import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
responseHistoryCounter = 0
for each in response.history: responseHistoryCounter += 1

print("Суммарное количество редиректов - ", responseHistoryCounter)
print("Итоговый URL - ", response.url)

