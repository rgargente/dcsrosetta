import guizero as gz


class DcsRosettaApp:
    def __init__(self):
        app = gz.App(title="Hello world", layout='grid', width=800)
        gz.Text(app, 'Yandex key: ', grid=[0, 0])
        yandex_key_t = gz.TextBox(app, 'Yandex', grid=[1, 0], width=100)
        gz.PushButton(app, text='Save', grid=[2, 0], width=7,
                      command=self.save_yandex_key)
        app.display()

    def save_yandex_key(self):
        pass


if __name__ == '__main__':
    app = DcsRosettaApp()
