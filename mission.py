import os
import shutil
import tempfile
import zipfile

from dcsdictionary import DcsDictionary


class Mission:
    DICTIONARY_PATH = 'l10n/DEFAULT/dictionary'

    def __init__(self, path):
        self.path = path

    def _unzip(self, dest_folder):
        with zipfile.ZipFile(self.path, 'r') as zip:
            zip.extractall(dest_folder)
            zip.close()

    def _zip(self, source_folder, dest_miz_path):
        if not os.path.exists(os.path.dirname(dest_miz_path)):
            os.mkdir(os.path.dirname(dest_miz_path))
        zipf = zipfile.ZipFile(dest_miz_path, mode='w')
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len(source_folder):])
        zipf.close()

    def translate(self, dest_miz: str = None, whole: bool = True, from_lang=None, to_lang=None):
        tmp = tempfile.mkdtemp()
        self._unzip(tmp)
        dest_trans_path = os.path.join(tmp, f'l10n/{to_lang.upper()}/')
        if os.path.exists(dest_trans_path):
            raise (Exception(f'It seems like this mission already has a "{to_lang}" translation!'))
        shutil.copytree(os.path.join(tmp, 'l10n/DEFAULT/'), dest_trans_path)
        dd = DcsDictionary.from_file_path(os.path.join(tmp, self.DICTIONARY_PATH))
        print('Translating mission...')
        if whole:
            try:
                tdd = dd.translate_whole(from_lang, to_lang)
            except Exception as e:
                print(e)
                tdd = dd.translate_item_by_item(from_lang, to_lang)
        else:
            tdd = dd.translate_item_by_item()
        tdd.save(os.path.join(tmp, f'l10n/{to_lang.upper()}/dictionary'))
        if dest_miz is None:
            dest_miz = self.path.replace('.miz', '_trans.miz')
        self._zip(tmp, dest_miz)
        print('New translated mission generated: {}'.format(dest_miz))
