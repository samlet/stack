class TransClipConf(object):
    def __init__(self, conf_file='/pi/conf/trans_clip.json'):
        import json_utils
        self.conf = json_utils.read_json_file(conf_file)

    def is_enabled(self, opt):
        """
        >>> import sagas.conf.conf as conf
        >>> cf=conf.TransClipConf('./conf/trans_clip.json')
        >>> print(cf.is_enabled('trans_cache'), cf.is_enabled('xx'))

        $ python -m sagas.conf.conf is_enabled print_not_matched

        :param opt:
        :return:
        """
        return opt in self.conf and self.conf[opt]

    @property
    def common_s(self):
        """
        $ python -m sagas.conf.conf common_s
        :return:
        """
        return self.conf['common_s']

    def servant(self, engine):
        servants = self.conf['servants']
        return servants[engine]

    def get_opt(self, opt, item_name):
        item_val=self.conf[opt]
        if item_name in item_val:
            return item_val[item_name]
        return item_val['*']

    def engine(self, lang):
        return self.get_opt('dialectors', lang)

    def servant_by_lang(self, lang):
        return self.servant(self.get_opt('dialectors', lang))

    def validate(self):
        """
        $ python -m sagas.conf.conf validate
        :return:
        """
        import sagas
        servants=self.conf['servants']
        sagas.print_rs([(k,v) for k,v in servants.items()], ['servant', 'url'])
        print(f"corenlp:    {self.servant('corenlp')}")
        print(f"spacy:      {self.servant('spacy')}")
        print(f"el_Greek:   {self.servant_by_lang('el')}")
        print(f"en_US:      {self.servant_by_lang('en')}")
        print(f"engine for zh: {self.engine('zh')}")
        print(f"ofbiz: {self.conf['ofbiz_servant']}")

"""
from sagas.conf.conf import cf
cf.conf['xx']
cf.common_s
cf.is_enabled('print_not_matched')
"""
cf=TransClipConf()

if __name__ == '__main__':
    import fire
    fire.Fire(TransClipConf)
