import json
import os
import shutil
import tempfile
import zipfile

from yandex_translate import YandexTranslate


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
    translator = YandexTranslate('trnsl.1.1.20181004T104638Z.0b0cac35b15caf05.17c474e1314fc98b6efeae0124aa1767f8b6594c')
    trans_dict = {}
    for k, v in dict.items():
        if v:
            trans_dict[k] = translator.translate(v, 'en')['text'][0]
        else:
            trans_dict[k] = v
    return trans_dict


def translate_miz(source_miz: str, dest_miz: str):
    tmp = tempfile.mkdtemp()
    unzip_mission(source_miz, tmp)
    shutil.copytree(os.path.join(tmp, 'l10n/DEFAULT/'),
                    os.path.join('l10n/EN/'))
    dict = load_dict(os.path.join(tmp, 'l10n/DEFAULT/dictionary'))
    save_dict(translate_dict(dict), 'l10n/EN/dictionary')
    zip_mission(tmp, dest_miz)
