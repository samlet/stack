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
