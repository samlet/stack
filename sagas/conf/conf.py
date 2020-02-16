import json_utils

def runtime_dir():
    import os
    return os.path.dirname(__file__)

class TransClipConf(object):
    def __init__(self):
        from sagas.conf.runtime import runtime
        conf_file=f"{runtime_dir()}/sagas_conf.json"
        overrides_file=f"{runtime_dir()}/sagas_overrides.json"

        self.conf = json_utils.read_json_file(conf_file)
        self.overrides_file=overrides_file
        if runtime.is_docker():
            self.update_by_overrides()

    def update_by_overrides(self):
        overrides=json_utils.read_json_file(self.overrides_file)
        for k, v in overrides.items():
            if '.' in k:
                parts = k.split('.')
                self.conf[parts[0]][parts[1]] = v
            else:
                self.conf[k] = v

    def is_enabled(self, opt):
        """
        >>> import sagas.conf.conf as conf
        >>> cf=conf.TransClipConf('./conf/sagas_conf.json')
        >>> print(cf.is_enabled('trans_cache'), cf.is_enabled('xx'))

        $ python -m sagas.conf.conf is_enabled print_not_matched

        :param opt:
        :return:
        """
        import os
        val=os.getenv(opt)
        if val is not None:
            return True if val.lower() in ('on', 'yes', 'true', '1') else False
        return opt in self.conf and self.conf[opt]

    def enable_opt(self, opt):
        self.conf[opt]=True

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
        import os
        return os.getenv('engine', self.get_opt('dialectors', lang))

    def servant_by_lang(self, lang):
        return self.servant(self.get_opt('dialectors', lang))

    def ensure(self, item):
        """
        $ python -m sagas.conf.conf ensure multilang
        => http://localhost:8095

        :param item:
        :return:
        """
        if item in self.conf:
            return self.conf[item]
        raise ValueError("Cannot find item value: " + item)

    def optional(self, item, defval):
        return self.conf[item] if item in self.conf else defval

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
        print(f"conf dir: {runtime_dir()}")
        print(f"root dir: {sagas.runtime_dir()}")

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
