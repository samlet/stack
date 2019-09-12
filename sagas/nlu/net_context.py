class EntitiesRequest(object):
    def __init__(self, req_json):
        self.sents = req_json['sents']
        self.lang = req_json['lang']

    def wrap_result(self, rs):
        import json
        data_y = json.dumps(rs, ensure_ascii=False)
        return data_y

    def empty_set(self):
        return '[]'

