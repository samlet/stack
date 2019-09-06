from sagas.nlu.ruleset import RuleSetRunner

if __name__ == '__main__':
    """
    $ python -m sagas.nlu.ruleset_main
    """
    rsr=RuleSetRunner()
    # rsr.rules_pkgs()
    rsr.test_all()


