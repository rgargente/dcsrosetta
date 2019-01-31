import os

import pytest

from dcsdictionary import DcsDictionary


@pytest.fixture()
def dcs_dict():
    return DcsDictionary.from_file_path('dictionary')


def test_load_dict(tmpdir):
    old_dict_path = 'dictionary'
    dict = DcsDictionary.from_file_path(old_dict_path)
    new_dict_path = os.path.join(tmpdir, 'newdict.txt')
    dict.save(new_dict_path)

    with open(old_dict_path, encoding='UTF-8') as f:
        old_content = f.read()
    with open(new_dict_path, encoding='UTF-8') as f:
        new_content = f.read()
    assert old_content.replace(" ", "") == new_content.replace(" ", "")


def test_translate_dict(dcs_dict):
    trans = dcs_dict.translate_item_by_item()
    assert len(dcs_dict.dict) == len(trans.dict)
    assert trans.dict['DictKey_ActionText_400'].startswith('Woodpecker 2 reports:')


def test_translate_whole(dcs_dict):
    trans = dcs_dict.translate_whole()
    assert len(dcs_dict.dict) == len(trans.dict)
    assert trans.dict['DictKey_ActionText_400'].startswith('Woodpecker 2 reports:')


def test_to_lua(dcs_dict):
    lua_dict = DcsDictionary.to_lua(dcs_dict.dict)
    new_dict = DcsDictionary.from_lua_str(lua_dict)
    assert dcs_dict == new_dict
