from typing import Text, Any, Dict, List, Union, Optional
import json
from sagas.conf.conf import load_class

class ListingsCli(object):
    def __init__(self):
        self.configs={}
        self.preloads={}

    def get_conf(self, conf:Text, item:Text) -> Dict[Text, Any]:
        import _jsonnet
        import io
        from os.path import expanduser

        if conf not in self.configs:
            conf_dir = expanduser('~/listings')
            encoding = "utf-8"
            filename = f"{conf_dir}/{conf}.jsonnet"
            with io.open(filename, encoding=encoding) as f:
                jsonnet_str = f.read()
            json_str = _jsonnet.evaluate_snippet(
                "snippet", jsonnet_str,
                ext_vars={})
            json_obj = json.loads(json_str)
            self.configs[conf]=json_obj

        json_obj=self.configs[conf]
        conf_cnt = json_obj[item]
        return conf_cnt

    def get_instance(self, conf_cnt:Dict[Text, Any]):
        type_name=conf_cnt['type']
        if type_name not in self.preloads:
            co_clz = load_class(type_name)
            # co=co_clz(conf_cnt)
            co = co_clz()
            co.preload()
            self.preloads[type_name] = co
        return self.preloads[type_name]

    def proc(self, conf, item, input):
        """
        $ python -m sagas.listings.listings_cli proc simple Simple \
            "Hugging Face is a technology company based in New York and Paris"
        $ python -m sagas.listings.listings_cli proc t5 T5_de \
            "Hugging Face is a technology company based in New York and Paris"
        $ python -m sagas.listings.listings_cli proc t5 T5_fr \
            "Hugging Face is a technology company based in New York and Paris"

        :param conf:
        :param item:
        :param input:
        :return:
        """
        from sagas.util.collection_util import to_obj
        conf_cnt=self.get_conf(conf, item)
        co = self.get_instance(conf_cnt)
        print(conf_cnt)
        return co.proc(to_obj(conf_cnt), input)

    def example(self, conf, item):
        """
        $ python -m sagas.listings.listings_cli example simple echo
        $ python -m sagas.listings.listings_cli example t5 fr
        $ list simple echo
        :param conf:
        :param item:
        :return:
        """
        conf_cnt = self.get_conf(conf, 'Examples')
        example_item=conf_cnt[item]
        r= self.proc(conf, example_item['conf'], example_item['input'])
        print(r)

        prof=self.get_conf(conf, example_item['conf'])
        if 'visualizer' in prof:
            vis=load_class(prof['visualizer'])
            vis().render(r.data)

listings=ListingsCli()

if __name__ == '__main__':
    import fire
    fire.Fire(listings)

