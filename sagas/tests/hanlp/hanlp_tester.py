from sagas.bots.hanlp_procs import hanlp

def test_py4j():
    raw='我是中学生'
    sentence = hanlp.j.HanLP.parseDependency(raw)
    wordArray = sentence.getWordArray()
    for word in wordArray:
        print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))

def test_grpc():
    from sagas.bots.hanlp_client import HanlpClient
    client=HanlpClient()
    client.disp_deps('苹果电脑可以运行开源阿尔法狗代码吗')

if __name__ == '__main__':
    test_py4j()
    print('------------------')
    test_grpc()

