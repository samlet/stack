from sagas.bots.hanlp_viz import HanlpProtoViz, entities_df

class HanlpExtractor(object):
    def __init__(self):
        self.viz = HanlpProtoViz(verbose=False)
        self.attrs=['t', 'mq', 'nr', 'nz', 'nrf', 'n']

    def sbv_vob(self, text):
        from termcolor import colored
        response = self.viz.hanlp.get_deps(text)
        rs=[]
        if 'zh_SBV|text' in response.coreGraph:
            v= response.coreGraph['zh_SBV|text']
            rs.append(colored(v, 'green'))
        if 'zh_VOB|head' in response.coreGraph:
            v=response.coreGraph['zh_VOB|head']
            rs.append(colored(v, 'red'))
        if 'zh_VOB|text' in response.coreGraph:
            v=response.coreGraph['zh_VOB|text']
            rs.append(colored(v, 'blue'))
        # for k, v in response.coreGraph.items():
        #     print(k, v)
        print(' '.join(rs))

    def to_df(self, text):
        """
        $ python -m sagas.nlu.extractor_hanlp to_df '我要找上星期销量最好的雨伞'
        $ python -m sagas.nlu.extractor_hanlp to_df '苹果电脑可以运行开源阿尔法狗代码吗'
        :param text:
        :return:
        """
        ## entities
        r = self.viz.extract(text)
        matches = sorted(r.entities, key=lambda _: _.start)
        spans = [_.entity+'_'+_.value for _ in matches
                 if _.entity in self.attrs
                 ]
        print("(%s)" % '; '.join(spans))
        self.sbv_vob(text)
        print(entities_df(matches))

if __name__ == '__main__':
    import fire
    fire.Fire(HanlpExtractor)

