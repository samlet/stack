def knp_deps(result):
    for bnst in result.bnst_list():
        parent = bnst.parent
        if parent is not None:
            child_rep = " ".join(mrph.repname for mrph in bnst.mrph_list())
            parent_rep = " ".join(mrph.repname for mrph in parent.mrph_list())
            print(child_rep, "->", parent_rep)

class KnpCli(object):
    def deps(self, sents):
        """
        $ python -m sagas.ja.knp_cli deps "望遠鏡で泳いでいる少女を見た。"
        :param sents:
        :return:
        """
        from sagas.ja.knp_helper import knp
        result = knp.parse(sents)
        knp_deps(result)
        print("bnst list", '-'*15)
        for bnst in result.bnst_list():
            print(f"{bnst.bnst_id}, {bnst.midasi}, {bnst.parent_id}, {bnst.repname}, {bnst.dpndtype}")

        print('\nbnst tree', '-'*15)
        result.draw_bnst_tree()

        print('\ntag tree', '-' * 15)
        result.draw_tag_tree()

    def parse(self, sents, output='console'):
        """
        $ python -m sagas.ja.knp_cli parse "望遠鏡で泳いでいる少女を見た。"
        $ python -m sagas.ja.knp_cli parse "どのおかずを注文したの？"
        :param sents:
        :param output:
        :return:
        """
        import sagas.ja.knp_helper as kh
        kh.outputer=output
        kh.parse_knp(sents)

if __name__ == '__main__':
    import fire
    fire.Fire(KnpCli)
