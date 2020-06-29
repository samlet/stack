import operator
from typing import Text, Any, Dict, List, Union

from cachetools import cachedmethod
from os.path import expanduser
import json_utils

def runtime_dir():
    import os
    return os.path.dirname(__file__)

class TransClipConf(object):
    def __init__(self):
        from sagas.conf.runtime import runtime
        from cachetools import LRUCache

        conf_file=f"{runtime_dir()}/sagas_conf.json"
        overrides_file=f"{runtime_dir()}/sagas_overrides.json"

        self.conf = json_utils.read_json_file(conf_file)
        self.overrides_file=overrides_file
        if runtime.is_docker():
            self.update_by_overrides()

        # self.cache = LRUCache(maxsize=1024)
        self.loaded_classes={}

    def update_by_overrides(self) -> None:
        overrides=json_utils.read_json_file(self.overrides_file)
        for k, v in overrides.items():
            if '.' in k:
                parts = k.split('.')
                self.conf[parts[0]][parts[1]] = v
            else:
                self.conf[k] = v

    def is_enabled(self, opt) -> bool:
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

    def enable_opt(self, opt) -> None:
        self.conf[opt]=True

    @property
    def user_home(self) -> Text:
        from pathlib import Path
        return str(Path.home())

    @property
    def conf_dir(self) -> Text:
        return expanduser(self.ensure('conf_dir'))

    @property
    def data_dir(self):
        return expanduser(self.ensure('data_dir'))

    @property
    def common_s(self):
        """
        $ python -m sagas.conf.conf common_s
        :return:
        """
        return self.conf['common_s']

    def servant(self, engine) -> Text:
        servants = self.conf['servants']
        return servants[engine]

    def get_opt(self, opt, item_name):
        item_val=self.conf[opt]
        if item_name in item_val:
            return item_val[item_name]
        return item_val['*']

    def engine(self, lang) -> Text:
        import os
        return os.getenv('engine', self.get_opt('dialectors', lang))

    def _cache_clz(self, clz:str):
        from sagas.util.loader import class_from_module_path
        if clz not in self.loaded_classes:
            self.loaded_classes[clz]=class_from_module_path(clz)
        return self.loaded_classes[clz]

    def get_bucket(self, entity) -> Any:
        clz= self.get_opt('buckets', entity)
        return self._cache_clz(clz)

    # @cachedmethod(operator.attrgetter('cache'))
    def extensions(self, ext:Text, item:Text) -> Any:
        ext_node=self.conf['extensions'][ext]
        clz=ext_node[item] if item in ext_node else ext_node['*']
        return self._cache_clz(clz)

    def pipelines(self, lang:Text) -> List[Any]:
        ext_node=self.conf['extensions']['anal.pipelines']
        classes=ext_node[lang] if lang in ext_node else ext_node['*']
        return [self._cache_clz(clz) for clz in classes]

    def classes(self, item:Text) -> List[Any]:
        ls=self.ensure(item)
        return [self._cache_clz(clz) for clz in ls]

    def servant_by_lang(self, lang):
        return self.servant(self.get_opt('dialectors', lang))

    @property
    def user(self) -> Text:
        return self.ensure('user')

    def ensure(self, item:Text) -> Any:
        """
        $ python -m sagas.conf.conf ensure multilang
        => http://localhost:8095

        :param item:
        :return:
        """
        if item in self.conf:
            return self.conf[item]
        raise ValueError("Cannot find item value: " + item)

    @property
    def delegates(self):
        return self.ensure('delegates')

    @property
    def comps(self):
        return self.ensure('comps_delegator')

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

def load_class(clz:str):
    return cf._cache_clz(clz)

if __name__ == '__main__':
    import fire
    fire.Fire(TransClipConf)
