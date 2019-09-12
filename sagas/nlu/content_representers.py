import io
def repr_duckling_body(data, iot=None):
    from dateutil.parser import parse
    for item in data:
        val = item['value']
        item_type = val['type']
        if item_type == 'value':
            print(item['body'], '=', val['grain'], parse(val['value']), file=iot)
        elif item_type == 'interval':
            print(val['from'], '-', val['to'], file=iot)
        else:
            print(f'unknown item type {item_type}', file=iot)

def repr_snips_body(data, iot=None):
    try:
        for item in data:
            print(f"{item['value']} - {item['entity_kind']}", file=iot)
            entity = item['entity']
            print(entity['grain'], entity['value'], file=iot)
    except:
        print('cannot represent data:')
        print(data)

content_reprs={'duckling':repr_duckling_body,
               'snips':repr_snips_body,
               }

def content_represent(cnt_type, body):
    sio = io.StringIO()
    if cnt_type in content_reprs:
        content_reprs[cnt_type](body, iot=sio)
        return sio.getvalue()
    return body

class ContentRepresenter(object):
    def __init__(self):
        self.parsers={}
    def extract_duckling_dt(self, text):
        """
        $ python -m sagas.nlu.content_representers extract_duckling_dt '上个星期编辑'
        $ python -m sagas.nlu.content_representers extract_duckling_dt '周五下午7点到8点'
        $ ses 'Nosotros comíamos con la familia para Navidad.'  # 以content_represent方式显示inspector返回的日期数据

        :param text:
        :return:
        """
        from sagas.nlu.inspectors import query_duckling
        from json_utils import pretty_json

        resp = query_duckling(text, 'zh')
        print(pretty_json(resp))
        print('-' * 25)
        print('dims', [d['dim'] for d in resp['data']])
        data=resp['data']

        content_reprs['duckling'](data)

    def extract_snips(self, text, lang):
        """
        $ python -m sagas.nlu.content_representers extract_snips "in three days" en
        :param text:
        :param lang:
        :return:
        """
        from snips_nlu_parsers import BuiltinEntityParser

        if lang in self.parsers:
            parser = self.parsers[lang]
        else:
            parser = BuiltinEntityParser.build(language=lang)
            self.parsers[lang] = parser
        parsing = parser.parse(text)
        # parsing = parser.parse("in three days")
        dims = [d['entity_kind'] for d in parsing]
        print(dims)
        content_reprs['snips'](parsing)

if __name__ == '__main__':
    import fire
    fire.Fire(ContentRepresenter)
