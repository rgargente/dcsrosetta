import os

from dcsdictionary import DcsDictionary
from mission import Mission


class CmpDictionary(DcsDictionary):
    def __init__(self):
        super()
        self.field_filter = lambda f: f.key.s.startswith('description') or f.key.s == 'file'

    def translate_item_by_item(self, from_lang, to_lang):
        """Translates the cmp file description"""
        # TODO Do like in the miz dict
        print('Translating campaign description...')
        desc = self.dict['description']
        lua_desc = '["description"] = "{}",'.format(desc)
        self.lua_str = self.lua_str.replace(lua_desc,
                                            lua_desc + '\n    ["description_{}"] = "{}",'.format(
                                                to_lang.upper(),
                                                self.translator.translate(desc, from_lang, to_lang)))

    def get_mizs(self):
        mizs = []
        for l in self.lua_str.splitlines():
            if '["file"]' in l:
                mizs.append(l.split('"')[3])
        mizs.sort()
        return mizs


class Campaign:
    def __init__(self, path: str):
        self.path = path
        self.cmp_dict = CmpDictionary.from_file_path(path)

    def translate(self, from_lang=None, to_lang=None):
        self.cmp_dict.translate_item_by_item(from_lang, to_lang)
        dir_path = os.path.join(os.path.dirname(self.path), 'trans/')
        if not os.path.exists(os.path.dirname(dir_path)):
            os.mkdir(os.path.dirname(dir_path))
        self.cmp_dict.save(os.path.join(dir_path, os.path.basename(self.path)))
        print('Translating campaign missions...')
        for miz_name in self.cmp_dict.get_mizs():
            miz_path = os.path.join(os.path.dirname(self.path), miz_name)
            Mission(miz_path).translate(os.path.join(dir_path, miz_name), from_lang=from_lang, to_lang=to_lang)
