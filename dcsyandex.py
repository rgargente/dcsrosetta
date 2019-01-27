import os

from yandex_translate import YandexTranslate


class DcsYandexTranlator:
    YANDEX_KEY_FILE = 'yandex_key.txt'

    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.YANDEX_KEY_FILE)
        with open(path) as f:
            key = f.read()
        self.translator = YandexTranslate(key)

    def translate(self, desc, lang):
        return self.translator.translate(desc, lang)

