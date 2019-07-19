import time
from sagas.nlu.google_translator import translate

def marks(t):
    if len(t)>0:
        return ','+' '.join(t)[1:]
    return ''
def process(source, target, text):
    options=set(['get_pronounce'])
    # options.add('get_pronounce')
    res,t = translate(text, source=source, target=target,
                      trans_verbose=False, options=options)
    # print(res, text, t[ips_idx])
    print('✁', '%s(%s %s)'%(text, res, ''.join(t.pronounce)))
    for sent in text.split(' '):
        res,t = translate(sent, source=source, target=target,
                          trans_verbose=False, options=options)
        # print(res, sent, t[ips_idx])
        print('%s(%s%s)'%(sent,res,marks(t.pronounce)), end =" ")
        time.sleep(0.05)
    print('.')

def analyse_vi(text):
    """
    analyse_vi('Tôi là sinh viên')
    :param text:
    :return:
    """
    target='zh'
    process('vi', target, text)

def analyse_th(text):
    """
    analyse_th('ฉันมีตู้เย็นสองตู้')
    :param text:
    :return:
    """
    target='zh'
    process('th', target, text)

def process_zh_vi(text, target='vi'):
    """
    process_zh_vi('我是一个学生')
    process_zh_vi('我是一个学生', 'th')
    :param text:
    :param target:
    :return:
    """
    import jieba
    source='zh-CN'
    res,t = translate(text, source=source, target=target,
                      trans_verbose=False)
    print('✁', '%s(%s %s)'%(text, res, ''.join(t.pronounce)))
    for sent in jieba.cut(text):
        res,t = translate(sent, source=source, target=target,
                          trans_verbose=False)
        print('%s(%s%s)'%(sent,res,marks(t.pronounce)), end =" ")
        time.sleep(0.05)
    print('.')

def process_en_vi(text, target='vi'):
    """
    process_en_vi('I am a student')
    # indonesian
    process_en_vi('I am a student', 'id')
    process_en_vi('I am a student', 'ar')
    # turkish
    process_en_vi('I am a student', 'tr')
    process_en_vi('I am a student', 'th')
    :param text:
    :param target:
    :return:
    """
    source='en'
    res,t = translate(text, source=source, target=target,
                      trans_verbose=False)
    print('✁', '%s(%s %s)'%(text, res, ''.join(t.pronounce)))
    for sent in text.split(' '):
        res,t = translate(sent, source=source, target=target,
                          trans_verbose=False)
        print('%s(%s%s)'%(sent,res,marks(t.pronounce)), end =" ")
        time.sleep(0.05)
    print('.')

def marks_th(t):
    if len(t)>0:
        return ','+t[0][1:]
    return ''

def process_en_th(text, target='th'):
    """
    process_en_th('I have two refrigerators')
    process_en_th('I have two refrigerators', 'ar')
    process_en_th('We are going to the park to play', 'ar')
    # hebrew
    process_en_vi('I have two refrigerators', 'iw')
    process_en_th('I have two refrigerators', 'hi')
    process_en_th('I am a student', 'hi')
    # greek language
    process_en_th('I am a student', 'el')
    process_en_th('I have two refrigerators', 'el')
    process_en_th('I have two refrigerators', 'ko')

    :param text:
    :param target:
    :return:
    """
    source='en'
    options=set(['get_pronounce'])
    res,t = translate(text, source=source, target=target,
                      trans_verbose=False, options=options)
    print('✁', '%s(%s %s)'%(text, res, ''.join(t.pronounce)))
    for sent in text.split(' '):
        res,t = translate(sent, source=source, target=target,
                          trans_verbose=False, options=options)
        print('%s(%s%s)'%(sent,res,marks_th(t.pronounce)), end =" ")
        time.sleep(0.05)
    print('.')



