from durable.lang import *
from durable.engine import Host
import sagas.tracker_fn as tc

with ruleset('verbs'):
    @when_all(m.text.matches('want.*'))
    def verb_want(c):
        c.s.matches = True
        print('verb matches pat -> {0}'.format(c.m.text))


    @when_all(m.amod_ref.anyItem(item.matches('.*thing.*, entity.*')))
    def amod_ref(c):
        c.s.amod_ref = True
        print('amod_ref pat -> {0}'.format(c.domains.amod))


    @when_all(m.xcomp.anyItem(item.text.matches('play') &
                              item.obj.anyItem(item.text.matches('music'))))
    def xcomp_play(c):
        c.s.xcomp_play = True
        # print ('xcomp pat -> {0}'.format(c.m.xcomp))
        print('xcomp pat')


    @when_all(m.nsubj.anyItem(item.text.imatches('I')))
    def subj_play(c):
        # print ('xcomp pat -> {0}'.format(c.m.domains.xcomp.text))
        print('nsubj pat')

ls = lambda l, e: [e] if l is None else l + [e]

with ruleset('chains'):
    @when_all(m.amod.anyItem(item.matches('.*thing.n.*, .*physical_entity.n.*')))
    def amod_with_thing(c):
        c.s.amod_with_thing = True
        c.s.amod = ls(c.s.amod, 'thing')
        print('amod thing -> {0}'.format(c.m.word))


    @when_all(m.amod.anyItem(item.matches('.*natural_object.n.*, .*object.n.*')))
    def amod_with_natural(c):
        c.s.amod_with_natural = True
        c.s.amod = ls(c.s.amod, 'natural')
        print('amod natural -> {0}'.format(c.m.word))


    @when_all( (m.ref=='_/xcomp/obj') & m.sepcs.anyItem(item.matches('.*sound.n.*, .*perception.n.*')))
    def cat_sound(c):
        c.s.spec_xcomp_obj = ls(c.s.spec_xcomp_obj, 'sound')
        # print('xcomp obj -> {0}'.format(c.m.word))
        c.assert_fact({'ref': c.m.ref, 'predicate': 'as', 'catalog': 'sound'})

    @when_all((m.ref == '_/xcomp/obj') & m.sepcs.anyItem(item.matches('.*video.n.*, .*visual_communication.n.*')))
    def cat_video(c):
        c.s.spec_xcomp_obj = ls(c.s.spec_xcomp_obj, 'video')
        c.assert_fact({'ref': c.m.ref, 'predicate': 'as', 'catalog': 'video'})


    @when_all((m.ref == '_/xcomp') & m.sepcs.anyItem(item.matches('.*perform.v.*')))
    def act_perform(c):
        c.s.spec_xcomp = ls(c.s.spec_xcomp, 'perform')
        c.assert_fact({'ref': c.m.ref, 'predicate': 'is', 'catalog': 'perform'})

    @when_all((m.ref == '_') & m.sepcs.anyItem(item.matches('.*desire.v.*')))
    def act_want(c):
        c.s.spec_verb = ls(c.s.spec_verb, 'willing')
        c.assert_fact({'ref': c.m.ref, 'predicate': 'is', 'catalog': 'willing'})

    @when_all(+m.ref & +m.lemma)
    def output_tokens(c):
        tc.emp('blue', 'word-> Fact: {0} {1} {2}'.format(c.m.ref, c.m.lemma, c.m.upos))


    @when_all(+m.ref & +m.predicate)
    def output_predicates(c):
        tc.emp('red', 'catalog-> Fact: {0} {1} {2}'.format(c.m.ref, c.m.predicate, c.m.catalog))

with ruleset('sents'):
    @when_all(m.nsubj.anyItem(item.upos.imatches('pron')))
    def subj_play(c):
        # print('nsubj is prop')
        c.assert_fact({'ref': 'nsubj', 'predicate': 'is', 'catalog': 'prop'})

    @when_all(m.spec_verb.anyItem(item =='willing') &
              m.spec_xcomp.anyItem(item == 'perform') &
              m.spec_xcomp_obj.anyItem(item=='video'))
    def perform_video(c):
        # c.s.intents = ls(c.s.intents, 'perform_video')
        c.s.intents = ls(c.s.intents, {'intent': 'perform_media', 'object_type': 'video'})

    # @when_all((m.lemma == 'want') &
    @when_all(m.spec_verb.anyItem(item == 'willing') &
              m.spec_xcomp.anyItem(item == 'perform') &
              m.spec_xcomp_obj.anyItem(item == 'sound'))
    def perform_sound(c):
        c.s.intents = ls(c.s.intents, {'intent':'perform_media', 'object_type':'sound'})

    @when_all(+m.ref & +m.predicate)
    def output_predicates(c):
        tc.emp('red', 'catalog-> Fact: {0} {1} {2}'.format(c.m.ref, c.m.predicate, c.m.catalog))

    @when_all(+m.text & +m.lemma)
    def output_tokens(c):
        tc.emp('blue', 'sents-> Fact: {0} {1}'.format(c.m.text, c.m.lemma))

# key is level, values are rule names
ents_group={"token": ['chains'],
                "sents": ['sents'],
                }

