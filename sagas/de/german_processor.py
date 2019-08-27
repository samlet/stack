class GermanProcessor(object):
    def digest(self, sents, engine='corenlp'):
        """
        $ python -m sagas.de.german_processor digest "Die Eltern mögen den Käse."
        $ python -m sagas.de.german_processor digest "Es gefällt ihm zu telefonieren."

        :param sents:
        :return:
        """
        import requests
        from sagas.conf.conf import cf
        # "Die Eltern mögen den Käse."
        data = {"sents": sents}
        response = requests.post(f'{cf.servant(engine)}/digest', json=data)
        print(response.status_code, response.json())

if __name__ == '__main__':
    import fire
    fire.Fire(GermanProcessor)

