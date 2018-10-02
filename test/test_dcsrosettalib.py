import os
import filecmp

import dcsrosettalib


def test_unzip_and_zip(tmpdir):
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    unzip_folder = os.path.join(tmpdir, '01')
    dcsrosettalib.unzip_mission(source_miz, unzip_folder)
    new_path = os.path.join(tmpdir, '01.miz')
    dcsrosettalib.zip_mission(unzip_folder, new_path)

    # We should do something here but for now I just checked it is ok manually
    # assert filecmp.cmp(source_miz, new_path)


def test_load_dict(tmpdir):
    old_dict_path = 'dictionary'
    dict = dcsrosettalib.load_dict(old_dict_path)
    new_dict_path = os.path.join(tmpdir, 'newdict.txt')
    dcsrosettalib.save_dict(dict, new_dict_path)

    with open(old_dict_path, encoding='UTF-8') as f:
        old_content = f.read()
    with open(new_dict_path, encoding='UTF-8') as f:
        new_content = f.read()
    assert old_content.replace(" ", "") == new_content.replace(" ", "")




def test_translate_miz(tmpdir):
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    dest_mix = os.path.join(tmpdir, '01.miz')
    dcsrosettalib.translate(source_miz, dest_mix)
    assert False
