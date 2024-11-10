import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

parsedJson = json.loads(json_text)
rootKey = 'messages'

if rootKey in parsedJson:
    rootObj = parsedJson[rootKey]
    print(rootObj[-1])
else:
    print(f"Ключа {rootKey} в JSON не обнаружено")
