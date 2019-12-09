from durable.lang import *
from durable.engine import Host

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



