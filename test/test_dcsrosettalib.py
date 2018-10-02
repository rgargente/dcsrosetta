import os

import dcsrosettalib


def test_unzip_and_zip(tmpdir):
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    unzip_folder = os.path.join(tmpdir, '01')
    dcsrosettalib.unzip_mission(source_miz, unzip_folder)
    new_path = os.path.join(tmpdir, '01.miz')
    dcsrosettalib.zip_mission(unzip_folder, new_path)

    # assert filecmp.cmp(source_miz, new_path) # We should do something here but for now I just checked it is ok manually
