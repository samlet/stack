class TransClipConf(object):
    def __init__(self):
        import json_utils
        self.conf = json_utils.read_json_file('./conf/trans_clip.json')

    def is_enabled(self, opt):
        """
        is_enabled('collect_verbs')
        :param opt:
        :return:
        """
        return opt in self.conf and self.conf[opt]


