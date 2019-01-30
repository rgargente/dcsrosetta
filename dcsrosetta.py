import PySimpleGUI as sg

from dcsyandex import DcsYandexTranlator


class DcsRosettaApp:
    layout = [[sg.Txt('Yandex key: '), sg.In(size=(90, 1), key='yandex_key', do_not_clear=True), sg.Button('Save')],
              [sg.Txt('Mission or campaign file: '), sg.Input(size=(80, 1)), sg.FileBrowse(file_types=(
                  ("DCS", "*.miz;*.cmp"),))],
              [sg.Button('Translate', size=(98, 1))],
              [sg.Output(size=(110, 30))]]

    def __init__(self):
        self.window = sg.Window('DCS Rosetta').Layout(self.layout)
        self.window.ReadNonBlocking()

        self.yandex_translator = DcsYandexTranlator()
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
