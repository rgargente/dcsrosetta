import pytest
import os

from dcsdictionary import DcsDictionary, CmpDictionary


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


@pytest.fixture()
def cmp():
    path = 'Pilotenalltag/Pilotenalltag.cmp'
    return CmpDictionary.from_file_path(path)


def test_translate_cmp_desc(cmp):
    cmp.translate_item_by_item()
    assert '["description_EN"] = "Everyday life of a pilot' in cmp.lua_str
    cmp.save('trans.cmp')


def test_get_cmp_mizs(cmp):
    mizs = cmp.get_mizs()
    assert len(mizs) == 16
    assert 'Pilotenalltag_01.miz' in mizs
    assert 'Pilotenalltag_16.miz' in mizs
