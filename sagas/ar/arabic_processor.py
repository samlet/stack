import time
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.google_translator import translate

def marks(tracker, lead=True):
    t=tracker.pronounce
    if len(t)>0:
        if lead:
            return ','+' '.join(t)[1:]
        else:
            return ' '.join(t)[1:]
    return ''

def process(source, target, text, ips_idx=0):
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
        print('%s(%s%s)'%(sent,res,marks(t)), end =" ")
        time.sleep(0.05)
    print('.')

# Set CSS properties for th elements in dataframe
th_props = [
  ('font-size', '20px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7f7f9')
  ]

# Set CSS properties for td elements in dataframe
td_props = [
  ('font-size', '16px'),
  ('max-width', '280px')
  ]

# Set table styles
# ⊕ [Styling — pandas 0.24.2 documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Fun-stuff)
styles = [
    dict(selector="th", props=th_props),
    dict(selector="td", props=td_props),
    dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '20pt')])
  ]
def process_df(source, target, text, with_styles=True):
    import sagas
    rs=[]
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
        print('%s(%s%s)'%(sent,res,marks(t)), end =" ")
        rs.append((sent,res,marks(t,False)))
        time.sleep(0.05)
    print('.')
    if with_styles:
        return sagas.to_df(rs, ['word', 'trans', 'ips']).style.set_table_styles(styles)
    else:
        return sagas.to_df(rs, ['word', 'trans', 'ips'])

def analyse_ar(text, disp_df=False):
    import sagas
    target='en'
    if disp_df:
        sagas.print_df(process_df('ar', target, text, with_styles=False))
    else:
        process('ar', target, text)
    NluTools().say(text, 'ar')

def marks_th(t):
    if len(t)>0:
        return ','+t[0][1:]
    return ''

class ArabicProcessor(object):
    def analyse(self, text, disp_df=True):
        """
        analyse_ar('أنا طالب جامعي صيني.')
        $ python -m sagas.ar.arabic_processor analyse 'أنا طالب جامعي صيني.'
        $ python -m sagas.ar.arabic_processor analyse 'لدي اثنين من الثلاجات'

        :param text:
        :return:
        """
        analyse_ar(text, disp_df)

    def analyse_en(self, sents):
        """
        $ python -m sagas.ar.arabic_processor analyse_en 'I am a student'
        :param sents:
        :return:
        """
        r, _ = translate(sents, source='en', target='ar')
        print('✔', r)
        self.analyse(r)

    def ka(self, *items):
        """
        $ python -m sagas.ar.arabic_processor ka I am a student
        $ ka I ask you for an answer.
        :param items:
        :return:
        """
        from sagas.nlu.nlu_tools import to_str
        sents = ' '.join([to_str(item) for item in items])
        self.analyse_en(sents)

    def deconstructing(self, text, target='ar'):
        """
        $ python -m sagas.ar.arabic_processor deconstructing 'I am a student'
        $ python -m sagas.ar.arabic_processor deconstructing 'I am a student' de
        $ python -m sagas.ar.arabic_processor deconstructing 'I am a student' fr
        $ python -m sagas.ar.arabic_processor deconstructing 'I am a student' es
        $ python -m sagas.ar.arabic_processor deconstructing 'I am a student' vi

        ## other langs: ru, ja, zh

        :param text:
        :param target:
        :return:
        """
        import sagas
        source = 'en'
        options = set(['get_pronounce', 'get_translations'])
        res, t = translate(text, source=source, target=target,
                           trans_verbose=False, options=options)
        print('✁', '%s(%s %s)' % (text, res, ''.join(t.pronounce)))
        for sent in text.split(' '):
            res, t = translate(sent, source=source, target=target,
                               trans_verbose=False, options=options)
            # print('%s(%s%s)' % (sent, res, marks_th(t.pronounce)), end=" ")
            print('%s(%s%s)' % (sent, res, marks_th(t.pronounce)))
            sagas.print_df(t.translations)
            time.sleep(0.05)
        print('.')

    def ana_ar(self, text):
        """
        $ python -m sagas.ar.arabic_processor ana_ar 'بسم الله الرحمن الرحيم'
        $ python -m sagas.ar.arabic_processor ana_ar 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'
        $ python -m sagas.ar.arabic_processor ana_ar "ادخل النص"
        :param text:
        :return:
        """
        from sagas.ar.arabycia import Arabycia
        ara = Arabycia(text)
        raw_data, data = ara.print_result()
        print(raw_data)
        print(data)

if __name__ == '__main__':
    import fire
    fire.Fire(ArabicProcessor)

