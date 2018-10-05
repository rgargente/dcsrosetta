import os

from dcsdictionary import DcsDictionary, CmpDictionary


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


def test_translate_dict():
    dd = DcsDictionary.from_file_path('dictionary')
    tdd = dd.translate()
    assert len(dd.dict) == len(tdd.dict)
    assert tdd.dict['DictKey_ActionText_400'].startswith('Woodpecker 2 reports:')


def test_translate_cmp_desc():
    path = 'Pilotenalltag/Pilotenalltag.cmp'
    cmp = CmpDictionary.from_file_path(path)
    cmp.translate()
    assert '["description_EN"] = "Everyday life of a pilot' in cmp.lua_str
    cmp.save('trans.cmp')
