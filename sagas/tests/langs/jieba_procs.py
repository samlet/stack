import jieba
import jieba.posseg as pseg

def user_dict():
    from sagas.conf import resource_path

    dictf = resource_path('dict_zh.txt')
    jieba.load_userdict(dictf)
    seg_list = jieba.cut("列出所有的采购订单")  # 默认是精确模式
    print(", ".join(seg_list))

def user_words():
    jieba.add_word('寄账单地址', tag='typ')
    jieba.add_word('新建', tag='srv')
    seg_list = jieba.cut("列出所有的寄账单地址")  # 默认是精确模式
    print(", ".join(seg_list))
    words = pseg.cut("新建所有的寄账单地址")
    for word, flag in words:
        print('%s %s' % (word, flag))

if __name__ == '__main__':
    user_dict()

