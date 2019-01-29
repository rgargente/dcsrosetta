import PySimpleGUI as sg

from dcsyandex import DcsYandexTranlator


class DcsRosettaApp:
    layout = [[sg.Txt('Yandex key: '), sg.In(size=(90, 1), key='yandex_key', do_not_clear=True), sg.Button('Save')]]

    def __init__(self):
        self.yandex_translator = DcsYandexTranlator()

        self.window = sg.Window('DCS Rosetta').Layout(self.layout)
        self.window.FindElement('yandex_key').Update(self.yandex_translator.key)
        self.run()

    def run(self):
        while True:
            event, values = self.window.Read()

            if event == 'Save':
                self.save_yandex_key(values['yandex_key'])
            else:
                break

    def save_yandex_key(self, value):
        self.yandex_translator.save_key(value)


if __name__ == '__main__':
    DcsRosettaApp()
