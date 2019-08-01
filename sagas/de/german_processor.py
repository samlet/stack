class GermanProcessor(object):
    def digest(self, sents):
        """
        $ python -m sagas.de.german_processor digest "Die Eltern mögen den Käse."
        $ python -m sagas.de.german_processor digest "Es gefällt ihm zu telefonieren."

        :param sents:
        :return:
        """
        import requests
        # "Die Eltern mögen den Käse."
        data = {"sents": sents}
        response = requests.post('http://localhost:8090/digest', json=data)
        print(response.status_code, response.json())

if __name__ == '__main__':
    import fire
    fire.Fire(GermanProcessor)
