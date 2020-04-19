import os
from sagas.conf import resource_path
from sagas.conf.conf import cf
from pyltp import Segmentor

MODELDIR = f'{cf.conf_dir}/ai/ltp/ltp_data_v3.4.0'

def test_dict():
    # self.segmentor.load(os.path.join(MODELDIR, "cws.model"))
    dictf = resource_path('dict_zh.txt')
    segmentor = Segmentor()  # 初始化实例
    segmentor.load_with_lexicon(os.path.join(MODELDIR, "cws.model"), dictf)
    # segmentor.load(os.path.join(MODELDIR, "cws.model"))
    words = segmentor.segment('列出派工单')  # fail: '列出所有的采购订单'
    print('\t'.join(words))
    segmentor.release()

def test_pos():
    from pyltp import Postagger
    postagger = Postagger()  # 初始化实例
    postagger.load(os.path.join(MODELDIR, "pos.model"))  # 加载模型

    words = ['列出', '所有','的', '采购订单']  # 分词结果
    postags = postagger.postag(words)  # 词性标注

    print('\t'.join(postags))
    postagger.release()  # 释放模型

if __name__ == '__main__':
    # test_dict()
    test_pos()

