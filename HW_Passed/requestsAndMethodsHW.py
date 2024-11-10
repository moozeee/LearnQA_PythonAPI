import string
import requests

requestTypes = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
reqUrl = "https://playground.learnqa.ru/ajax/api/compare_query_type"


def testfunc(reqtype: string, method: string):
    match reqtype:
        case "GET":
            rt = (requests.get(reqUrl, params={'method': method}).text, reqtype, method)
            return rt
        case "POST":
            rt = (requests.post(reqUrl, data={'method': method}).text, reqtype, method)
            return rt
        case "PUT":
            rt = (requests.put(reqUrl, data={'method': method}).text, reqtype, method)
            return rt
        case "DELETE":
            rt = (requests.delete(reqUrl, data={'method': method}).text, reqtype, method)
            return rt
        case "HEAD":
            rt = (requests.head(reqUrl, data={'method': method}).text, reqtype, method)
            return rt
        case "OPTIONS":
            rt = (requests.options(reqUrl, data={'method': method}).text, reqtype, method)
            return rt


res_without_method = requests.post(reqUrl)
print("Если отправить POST запрос без параметра method то возвращается ", res_without_method.text)

res_head = requests.head(reqUrl, data={'method': 'HEAD'})
print("Если отправить HEAD запрос то возвращается ", res_head.text)

res_correct_method = requests.post(reqUrl, data={'method': 'POST'})
print("Если отправить POST запрос c правильным method то возвращается ", res_correct_method.text)

for i in range(0, len(requestTypes)):
    for j in range(0, len(requestTypes)):
        res = testfunc(requestTypes[i], requestTypes[j])
        if (res[0].__contains__("success")) and (res[1] != res[2]):
            print("Метод возвращает ", res[0], " если тип запроса ", requestTypes[i], " а method = ", requestTypes[j])
