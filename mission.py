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
        zipf = zipfile.ZipFile(dest_miz_path, mode='w')
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len(source_folder):])
        zipf.close()

    def translate_miz(self, dest_miz: str):
        tmp = tempfile.mkdtemp()
        self._unzip(tmp)
        shutil.copytree(os.path.join(tmp, 'l10n/DEFAULT/'),
                        os.path.join(tmp, 'l10n/EN/'))
        dd = DcsDictionary.from_file_path(os.path.join(tmp, self.DICTIONARY_PATH))
        tdd = dd.translate()
        tdd.save(os.path.join(tmp, 'l10n/EN/dictionary'))
        self._zip(tmp, dest_miz)
