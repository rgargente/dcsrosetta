from luaparser import ast

from dcsyandex import DcsYandexTranlator


class DcsDictionary:
    translator = DcsYandexTranlator()

    @classmethod
    def from_file_path(cls, path, field_filter=None):
        dd = cls()
        if field_filter:
            dd.field_filter = field_filter
        dd._load_dict(path)
        return dd

    @classmethod
    def from_dict(cls, dict, lua_str, field_filter=None):
        dd = cls()
        dd.dict = dict
        dd.lua_str = lua_str
        if field_filter:
            dd.field_filter = field_filter
        return dd

    def __init__(self):
        self.dict = None
        self.lua_str = None
        self.field_filter = lambda f: True

    def __eq__(self, other):
        return self.dict == other.dict \
               and self.lua_str == other.lua_str \
               and self.field_filter == other.field_filter

    def __ne__(self, other):
        return not self.__eq__(other)

    def _load_dict(self, dict_path):
        with open(dict_path, encoding='UTF-8') as f:
            self.lua_str = f.read()
        lua = ast.parse(self.lua_str)
        fields = lua.body.body[0].values[0].fields

        keys = [f.key.s for f in fields if self.field_filter(f)]
        values = [f.value.s for f in fields if self.field_filter(f)]
        self.dict = dict(zip(keys, values))

    def translate_item_by_item(self):
        """
        Translates a dictionary making one translation request per item.
        WARNING: Slow! Better use translate_whole. Kept in case the other method fails
        :return: a translated DcsDictionary
        """
        trans_dict = {}
        trans_str = self.lua_str
        count = len(self.dict)
        i = 0
        for k, v in self.dict.items():
            i += 1
            print(f'Translating {i} of {count}')
            if v:
                t = self.translator.translate(v, 'en')['text'][0]
                trans_str = trans_str.replace(v, t)
                trans_dict[k] = t
            else:
                trans_dict[k] = v
        return self.from_dict(trans_dict, trans_str)

    def translate_whole(self):
        """
        Translates a dictionary making one translation request for the whole dictionary. It's faster this way.
        WARNING: If it doesn't work use
        :return: a translated DcsDictionary
        """
        whole_text = '. '.join('[[[*** {} ***]]]'.format(v) for v in self.dict.values())
        trans_whole = self.translator.translate(whole_text, 'en')['text'][0]
        values = [v.strip() for v in trans_whole.split('***]]]. [[[***')]
        assert len(self.dict) == len(values)
        values[0] = values[0][7:]
        values[-1] = values[-1][:-7]
        trans_dict = {z[0]: z[1] for z in zip(self.dict.keys(), values)}

        trans_str = self.lua_str
        for k, v in self.dict.items():
            if v:
                trans_str = trans_str.replace(v, trans_dict[k])

        return self.from_dict(trans_dict, trans_str)

    def save(self, dest_path):
        with open(dest_path, 'w', encoding='UTF-8') as f:
            f.write(self.lua_str)


class CmpDictionary(DcsDictionary):
    def __init__(self):
        super()
        self.field_filter = lambda f: f.key.s.startswith('description') or f.key.s == 'file'

    def translate_item_by_item(self):
        """Translates the cmp file description"""
        desc = self.dict['description']
        lua_desc = '["description"] = "{}",'.format(desc)
        self.lua_str = self.lua_str.replace(lua_desc,
                                            lua_desc + '\n    ["description_EN"] = "{}",'.format(
                                                self.translator.translate(desc, 'en')['text'][0]))

    def get_mizs(self):
        mizs = []
        for l in self.lua_str.splitlines():
            if '["file"]' in l:
                mizs.append(l.split('"')[3])
        return mizs
