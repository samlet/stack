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

content_reprs={'duckling':repr_duckling_body}
def content_represent(cnt_type, body):
    sio = io.StringIO()
    if cnt_type in content_reprs:
        content_reprs['duckling'](body, iot=sio)
        return sio.getvalue()
    return body

class ContentRepresenter(object):
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

if __name__ == '__main__':
    import fire
    fire.Fire(ContentRepresenter)
