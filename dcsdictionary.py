from luaparser import ast

from dcsyandex import DcsYandexTranlator
import io


class DcsDictionary:
    translator = DcsYandexTranlator()

    @classmethod
    def from_file_path(cls, path, field_filter=None):
        dd = cls()
        if field_filter:
            dd.field_filter = field_filter
        with open(path, encoding='UTF-8') as f:
            lua_str = f.read()
        dd._load_dict(lua_str)
        return dd

    @classmethod
    def from_dict(cls, dict, field_filter=None):
        dd = cls()
        dd.dict = dict
        dd.lua_str = cls.to_lua(dict)
        if field_filter:
            dd.field_filter = field_filter
        return dd

    @classmethod
    def from_lua_str(cls, lua_str: str):
        dd = cls()
        dd._load_dict(lua_str)
        return dd

    def __init__(self):
        self.dict = None
        self.lua_str = None
        self.field_filter = lambda f: True

    def __eq__(self, other):
        return self.dict == other.dict

    def __ne__(self, other):
        return not self.__eq__(other)

    def _load_dict(self, lua_str):
        self.lua_str = lua_str
        lua = ast.parse(lua_str)
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
        count = len(self.dict)
        i = 0
        for k, v in self.dict.items():
            i += 1
            print(f'Translating {i} of {count}')
            if v:
                t = self.translator.translate(v, 'en')['text'][0]
                trans_dict[k] = t
            else:
                trans_dict[k] = v
        return self.from_dict(trans_dict)

    def translate_whole(self):
        """
        Translates a dictionary making one translation request for the whole dictionary. It's faster this way.
        WARNING: If it doesn't work use translate_item_by_item
        :return: a translated DcsDictionary
        """

        # Using less symbols ([* *]) seems to increase the probabilities of the translator being confused
        whole_text = '. '.join('[[** {} **]]'.format(v) for v in self.dict.values() if v)
        trans_whole = self.translator.translate(whole_text, 'en')['text'][0]
        trans_values = [v.strip() for v in trans_whole.split('**]]. [[**')]
        trans_values[0] = trans_values[0][5:]
        trans_values[-1] = trans_values[-1][:-5]
        trans_dict = {}
        trans_values_iter = iter(trans_values)
        for k, v in self.dict.items():
            if v:
                trans_dict[k] = next(trans_values_iter)
            else:
                trans_dict[k] = ''
        return self.from_dict(trans_dict, self.to_lua(trans_dict))

    def save(self, dest_path):
        with open(dest_path, 'w', encoding='UTF-8') as f:
            f.write(self.lua_str)

    @classmethod
    def to_lua(cls, dict):
        strio = io.StringIO()
        strio.write('dictionary = \n')
        strio.write('{\n')
        for key, value in dict.items():
            value = value.strip()
            if value.endswith('\\'):  # This caused a huge amount of headaches!
                value = value[:-1]
            strio.write(f'    ["{key}"] = "{value}",\n')
        strio.write('} -- end of dictionary\n')
        strio.write('')
        return strio.getvalue()


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
