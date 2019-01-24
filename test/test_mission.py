import os
import pytest

from mission import Mission


@pytest.fixture()
def mission():
    source_miz = 'Pilotenalltag/Pilotenalltag_01.miz'
    return Mission(source_miz)


def test_unzip_and_zip(mission, tmpdir):
    unzip_folder = os.path.join(tmpdir, '01')
    mission._unzip(unzip_folder)
    new_path = os.path.join(tmpdir, '01.miz')
    mission._zip(unzip_folder, new_path)

    # We should do something here but for now I just checked it is ok manually
    # assert filecmp.cmp(source_miz, new_path)


def test_translate_miz_whole(mission, tmpdir):
    dest_miz = '01.miz'
    mission.translate_miz(dest_miz, whole=True)
    translated_miz = Mission(dest_miz)
    translated_miz._unzip(tmpdir)
    pass


# TODO Refactor this
def test_translate_miz_steps(mission, tmpdir):
    dest_miz = '01.miz'
    mission.translate_miz(dest_miz, whole=False)
    translated_miz = Mission(dest_miz)
    translated_miz._unzip(tmpdir)
    pass
