import requests
import pytest


class TestFirstAPI:
    names = [("Vitalii"), ("Arseniy"), ("")]
    @pytest.mark.parametrize("name", names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {"name": name}

        response = requests.get(url, params=data)
        assert response.status_code == 200, f"Статус код не 200"

        response_dict = response.json()
        assert "answer" in response_dict, f"В ответе на запрос нет слова answer"

        if len(name) == 0:
            expected_response_text = f"Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, "Текст в ответе на запрос некорректный"
