from py4j.java_gateway import JavaGateway, GatewayParameters
import py4j

def f(object, fld):
    return py4j.java_gateway.get_field(object, fld)

class TimeNlp(object):
    def __init__(self):
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(address='localhost', port=25333))
        self.analyst = self.gateway.entry_point.getTimeAnalyst()

    def parse(self, text, rel=None):
        """
        $ python -m sagas.zh.timenlp_procs parse "周五下午7点到8点" "2017-07-19-00-00-00"
        :param text:
        :param rel:
        :return:
        """
        DateUtil = self.gateway.jvm.com.time.util.DateUtil()
        normalizer = self.analyst.getNormalizer()
        if rel is None:
            normalizer.parse(text)
        else:
            normalizer.parse(text, rel)
        units = normalizer.getTimeUnit()
        print(f".. analyse {text}", f"with {rel}" if rel is not None else "")
        for unit in units:
            expr = f(unit, "Time_Expression")
            print(f"时间文本:{expr}, 对应时间: {DateUtil.formatDateDefault(unit.getTime())}")

timenlp=TimeNlp()

if __name__ == '__main__':
    import fire
    fire.Fire(TimeNlp)
