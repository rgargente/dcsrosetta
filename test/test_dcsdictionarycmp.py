import pytest

from dcsdictionarycmp import CmpDictionary


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
