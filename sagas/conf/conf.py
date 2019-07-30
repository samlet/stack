class TransClipConf(object):
    def __init__(self):
        import json_utils
        self.conf = json_utils.read_json_file('./conf/trans_clip.json')

    def is_enabled(self, opt):
        """
        import sagas.conf.conf as conf
        cf=conf.TransClipConf()
        print(cf.is_enabled('trans_cache'), cf.is_enabled('xx'))

        :param opt:
        :return:
        """
        return opt in self.conf and self.conf[opt]

cf=TransClipConf()

