class ListingsCli(object):
    def get_conf(self, conf, item):
        import json
        import _jsonnet
        import io
        from os.path import expanduser

        conf_dir = expanduser('~/listings')
        encoding = "utf-8"
        filename = f"{conf_dir}/{conf}.jsonnet"
        with io.open(filename, encoding=encoding) as f:
            jsonnet_str = f.read()
        json_str = _jsonnet.evaluate_snippet(
            "snippet", jsonnet_str,
            ext_vars={})
        json_obj = json.loads(json_str)

        conf_cnt = json_obj[item]
        return conf_cnt

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
        from sagas.conf.conf import load_class
        conf_cnt=self.get_conf(conf, item)
        co_clz = load_class(conf_cnt['type'])
        co = co_clz(conf_cnt)
        print(co.conf)
        return co.proc(input)

    def example(self, conf, item):
        """
        $ python -m sagas.listings.listings_cli example simple echo
        $ python -m sagas.listings.listings_cli example t5 fr

        :param conf:
        :param item:
        :return:
        """
        conf_cnt = self.get_conf(conf, 'Examples')
        example_item=conf_cnt[item]
        return self.proc(conf, example_item['conf'], example_item['input'])

if __name__ == '__main__':
    import fire
    fire.Fire(ListingsCli)

