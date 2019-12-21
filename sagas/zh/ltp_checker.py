from sagas.nlu.uni_impl_ltp import LtpParserImpl


class LtpChecker(object):
    def procs(self, sents):
        """
        $ python -m sagas.zh.ltp_checker procs '中国进出口银行与中国银行加强合作。'
        :param sents:
        :return:
        """
        from pprint import pprint
        result=LtpParserImpl('zh')(sents)
        pprint(result)

if __name__ == '__main__':
    import fire
    fire.Fire(LtpChecker)

