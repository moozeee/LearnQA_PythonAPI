import requests
import pytest


class TestShortPhraseAssert:
    def test_short_phrase_assert(self):

        input_text = input("Введите любую фразу короче 15 символов: ")
        input_text_length = len(input_text)
        assert input_text_length < 15, "Введенная фраза меньше 15 символов в длину"
