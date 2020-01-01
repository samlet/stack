import sagas.tracker_fn as tc
from sagas.nlu.operators import ud
from sagas.nlu.predicts import predicate
from sagas.nlu.ruleset_procs import get_subj_domain, get_aux_domain
from sagas.conf.conf import cf
from sagas.nlu.ruleset_procs import parse_sents, equals, group_by, children

class PredictSamples(object):
    def check_domains(self, domains, lang):
        final_rs=[]
        for el in domains:
            tc.emp('yellow', f"`{el['lemma']}` >> *{el['dc']['lemma']}*")
            r1 = predicate(el, ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')], lang)
            # r2=predicate(el, ud.__cat('be') >> [ud.nsubj('what'), ud.dc_cat('animal/object')], lang)
            result=all([r[0] for r in r1])
            final_rs.append(result)
            tc.emp('green' if result else 'red', [r[0] for r in r1], result)
        return any(final_rs)

class PredictsCli(object):
    def check_subj(self, sents, lang):
        """
        $ python -m sagas.nlu.predicts_cli check_subj 'Яблоко - это здоровый фрукт.' ru
        :param sents:
        :param lang:
        :return:
        """
        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)

        domains = get_subj_domain(doc_jsonify)
        ps=PredictSamples()
        tc.emp('cyan', f"result: {ps.check_domains(domains, lang)}")

    def check_aux(self, sents, lang):
        """
        $ python -m sagas.nlu.predicts_cli check_aux 'what will be the weather in three days?' en
        :param sents:
        :param lang:
        :return:
        """
        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)
        domains = get_aux_domain(doc_jsonify)
        ps = PredictSamples()
        tc.emp('cyan', f"result: {ps.check_domains(domains, lang)}")

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(PredictsCli)

