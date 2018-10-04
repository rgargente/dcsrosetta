import os
import shutil
import tempfile
import zipfile

from dcsdictionary import DcsDictionary


def unzip_mission(source_miz, dest_folder):
    with zipfile.ZipFile(source_miz, 'r') as zip:
        zip.extractall(dest_folder)
        zip.close()


def zip_mission(source_folder, dest_miz_path):
    zipf = zipfile.ZipFile(dest_miz_path, mode='w')
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path[len(source_folder):])
    zipf.close()


def translate_miz(source_miz: str, dest_miz: str):
    tmp = tempfile.mkdtemp()
    unzip_mission(source_miz, tmp)
    shutil.copytree(os.path.join(tmp, 'l10n/DEFAULT/'),
                    os.path.join(tmp, 'l10n/EN/'))
    dd = DcsDictionary.from_file_path(os.path.join(tmp, 'l10n/DEFAULT/dictionary'))
    tdd = dd.translate()
    tdd.save(os.path.join(tmp, 'l10n/EN/dictionary'))
    zip_mission(tmp, dest_miz)
