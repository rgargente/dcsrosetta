import guizero as gz

from dcsyandex import DcsYandexTranlator


class DcsRosettaApp:
    def __init__(self):
        self.yandex_translator = DcsYandexTranlator()

        app = gz.App(title="Hello world", layout='grid', width=800)
        gz.Text(app, 'Yandex key: ', grid=[0, 0])
        self.yandex_key_t = gz.TextBox(app,
                                       text=self.yandex_translator.key,
                                       grid=[1, 0], width=100)
        gz.PushButton(app, text='Save', grid=[2, 0], width=7,
                      command=self.save_yandex_key)
        app.display()

    def save_yandex_key(self):
        self.yandex_translator.save_key(self.yandex_key_t.value)


if __name__ == '__main__':
    DcsRosettaApp()
