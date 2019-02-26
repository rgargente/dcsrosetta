from threading import Thread

import PySimpleGUI as sg

from campaign import Campaign
from dcsyandex import DcsYandexTranlator
from mission import Mission
from paths import resource_path


class DcsRosettaApp:
    layout = [[sg.Txt('Yandex key: '), sg.In(size=(90, 1), key='yandex_key', do_not_clear=True), sg.Button('Save')],
              [sg.Txt('Mission or campaign file: '), sg.Input(size=(80, 1), key='path', do_not_clear=True),
               sg.FileBrowse(file_types=(("DCS", "*.miz;*.cmp"),))],
              [sg.Txt('Original language: '), sg.InputCombo(key='from_lang', values=['Auto'], enable_events=True),
               sg.Txt('Translated language: '), sg.InputCombo(key='to_lang', values=['en'], size=(2, 1))],
              [sg.Button('Translate', size=(98, 1))],
              [sg.Output(size=(110, 30))]]

    def __init__(self):
        self.window = sg.Window('DCS Rosetta', icon=resource_path('rosetta.ico')).Layout(self.layout)
        self.window.Read(timeout=0)

        self.yandex_translator = DcsYandexTranlator()
        self.window.FindElement('yandex_key').Update(self.yandex_translator.key)
        self.langs_dict = self.yandex_translator.get_langs()
        self.window.FindElement('from_lang').Update(values=['Auto'] + list(self.langs_dict.keys()))

        self.run()

    def _get_langs_kwargs(self, values):
        return {'from_lang': values['from_lang'],
                'to_lang': values['to_lang']}

    def run(self):
        while True:
            event, values = self.window.Read()
            if event == 'Save':
                self.save_yandex_key(values['yandex_key'])
            elif event == 'from_lang':
                self.change_languages(values['from_lang'])
            elif event == 'Translate':
                try:
                    path = values['path']
                    if path.endswith('.miz'):
                        miz = Mission(path)
                        Thread(group=None, target=miz.translate, kwargs=self._get_langs_kwargs(values)).start()
                    else:
                        cmp = Campaign(path)
                        Thread(group=None, target=cmp.translate, kwargs=self._get_langs_kwargs(values)).start()
                except Exception as e:
                    print(e)

    def save_yandex_key(self, value):
        self.yandex_translator.save_key(value)

    def change_languages(self, from_lang):
        self.window.FindElement('to_lang').Update(values=self.langs_dict[from_lang])


if __name__ == '__main__':
    DcsRosettaApp()
