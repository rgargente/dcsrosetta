import os

from dcsdictionary import DcsDictionary


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


def test_load_cmp_dict():
    path = 'Pilotenalltag/Pilotenalltag.cmp'
    dict = DcsDictionary.from_file_path(path, 'campaign')
    assert False


def test_translate_dict():
    dd = DcsDictionary.from_file_path('dictionary')
    tdd = dd.translate()
    assert len(dd.dict) == len(tdd.dict)
    assert tdd.dict['DictKey_ActionText_400'].startswith('Woodpecker 2 reports:')
