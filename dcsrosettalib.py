import json
import os
import tempfile
import zipfile
from googletrans import Translator


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


def load_dict(dict_path):
    with open(dict_path, encoding='UTF-8') as f:
        s = f.read()
    s = s.replace('\n', '')
    s = s.replace('dictionary =', '')
    s = s.replace('["', '"').replace('"]', '"')
    s = s.replace('=', ':')
    s = s.replace(',} -- end of dictionary', '}')
    s = s.replace('\\', '\\\\')  # If we don't do this one slash ends up looking the same as two
    return eval(s)


def save_dict(dict: {}, dest_path):
    s = json.dumps(dict, indent=4, ensure_ascii=False)
    s = 'dictionary = \n' + s
    s = s.replace('"DictKey_', '["DictKey_').replace('": ', '"] = ')
    s = s.replace('\\\\', '\\\n')
    s = s.replace('"\n}', '",\n} -- end of dictionary\n')
    with open(dest_path, 'w', encoding='UTF-8') as f:
        f.write(s)


def translate_dict(dict: {}):
    translator = Translator()
    trans_dict = {}
    for k, v in dict.items():
        trans_dict[k] = translator.translate(v, dest='en').text
    return trans_dict


def translate(source_miz: str, dest_miz: str):
    tmp = tempfile.mkdtemp()
    unzip_mission(source_miz, tmp)

    dict = load_dict(os.path.join(tmp, 'l10n/DEFAULT/dictionary'))

    zip_mission(tmp, dest_miz)
