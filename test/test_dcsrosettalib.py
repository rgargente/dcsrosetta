import os

import dcsrosettalib


def test_unzip_and_zip(tmpdir):
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    unzip_folder = os.path.join(tmpdir, '01')
    dcsrosettalib.unzip_mission(source_miz, unzip_folder)
    new_path = os.path.join(tmpdir, '01.miz')
    dcsrosettalib.zip_mission(unzip_folder, new_path)

    # We should do something here but for now I just checked it is ok manually
    # assert filecmp.cmp(source_miz, new_path)


def test_translate_miz(tmpdir):
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    dest_mix = '01.miz'
    dcsrosettalib.translate_miz(source_miz, dest_mix)
    assert False
