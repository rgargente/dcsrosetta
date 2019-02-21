import os

from yandex.Translater import Translater

from paths import get_app_path


class DcsYandexTranlator:
    YANDEX_KEY_FILE = os.path.join(get_app_path(), 'yandex_key.txt')

    def __init__(self):
        self.key = None
        try:
            self.load_key()
        except:
            self.translator = None

    def load_key(self):
        with open(self.YANDEX_KEY_FILE) as f:
            self.key = f.read()
        self.translator = Translater()
        self.translator.set_key(self.key)
        print('Yandex key loaded')

    def save_key(self, key: str):
        with open(self.YANDEX_KEY_FILE, 'w') as f:
            f.write(key)
        print("Yandex key saved")

    def translate(self, desc, lang):
        self.translator.set_text(desc)
        self.translator.set_from_lang(self.translator.detect_lang())
        self.translator.set_to_lang('en')
        response = self.translator.translate()
        print('Received response from Yandex')
        return response
