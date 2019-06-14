from client_wrapper import ServiceClient

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service
import logging

logger = logging.getLogger(__name__)

class HanlpClient(object):
    def __init__(self, host='localhost', port=10052):
        logger.info("connect to hanlp provider %s %d ..."%(host, port))
        self.client=ServiceClient(nlp_service, 'NlpProcsStub', host, port)

    def get_deps(self, text):
        request = nlp_messages.NlTexts(texts=[nlp_messages.NlText(text=text)])
        response = self.client.GetDependencyGraph(request)
        return response

    def disp_deps(self, text):
        """
        $ python -m sagas.bots.hanlp_client disp_deps '苹果电脑可以运行开源阿尔法狗代码吗'
        :param text:
        :return:
        """
        response=self.get_deps(text)
        for k,v in response.coreGraph.items():
            print(k,v)

    def put_deps(self, sents, props):
        response = self.get_deps(sents)
        for k, v in response.coreGraph.items():
            props[k]=v

if __name__ == '__main__':
    import fire
    fire.Fire(HanlpClient)

