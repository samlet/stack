import io
import logging
import traceback

logger = logging.getLogger(__name__)

def repr_duckling_body(data, iot=None):
    """
    对于duckling的分析结果的解读可以参考这个函数来进行
    :param data:
    :param iot:
    :return:
    """
    from dateutil.parser import parse
    try:
        for item in data:
            dim = item['dim']
            val = item['value']
            item_type = val['type']
            if dim=='number':
                print(f"{item_type}: {val['value']}")
            else:
                if item_type == 'value':
                    grain=val['grain'] if 'grain' in val else val['unit']
                    grain_val=val['value']
                    print(item['body'], '=', grain,
                          parse(grain_val) if isinstance(grain_val, str) else grain_val,
                          file=iot)
                elif item_type == 'interval':
                    print(val['from'], '-', val['to'], file=iot)
                else:
                    print(f'unknown item type {item_type}', file=iot)
    except Exception as e:
        logger.error(
            "Failed to parse text '{}'. "
            "Error: {}".format(data, e))

def repr_snips_body(data, iot=None):
    entity_procs={'InstantTime': lambda ent: print(f"{ent['grain']} : {ent['value']}", file=iot),
                  'TimeInterval': lambda ent: print(f"from {ent['from']} to {ent['to']}", file=iot),
                  }
    try:
        for item in data:
            print(f"{item['value']} - {item['entity_kind']}", file=iot)
            entity = item['entity']
            # print(entity['grain'], entity['value'], file=iot)
            entity_procs[entity['kind']](entity)
    except Exception as e:
        logger.error(
            "Failed to parse text '{}'. "
            "Error: {}".format(data, e))
        # print('cannot represent data:')
        traceback.print_tb(e.__traceback__)

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
    def extract_duckling_dt(self, text, lang='zh', verobse=False):
        """
        将duckling的的解析结果以可读形式表示出来:
        $ python -m sagas.nlu.content_representers extract_duckling_dt '上个星期编辑'
        $ python -m sagas.nlu.content_representers extract_duckling_dt '周五下午7点到8点'
        $ python -m sagas.nlu.content_representers extract_duckling_dt '金曜日の午後7時から午後8時' ja
        $ python -m sagas.nlu.content_representers extract_duckling_dt 'fifty damage' en
        $ ses 'Nosotros comíamos con la familia para Navidad.'  # 以content_represent方式显示inspector返回的日期数据

        :param text:
        :return:
        """
        from sagas.nlu.inspectors import query_duckling
        from json_utils import pretty_json

        resp = query_duckling(text, lang)
        if verobse:
            print(pretty_json(resp))
            print('-' * 25)
        print('dims', [d['dim'] for d in resp['data']])
        data=resp['data']

        content_reprs['duckling'](data)

    def extract_snips(self, text, lang):
        """
        $ python -m sagas.nlu.content_representers extract_snips "in three days" en
        $ python -m sagas.nlu.content_representers extract_snips '금요일 오후 7 시부 터 오후 8시' ko
        $ python -m sagas.nlu.content_representers extract_snips '先週' ja
        $ python -m sagas.nlu.content_representers extract_snips '金曜日の午後7時から午後8時まで' ja
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
