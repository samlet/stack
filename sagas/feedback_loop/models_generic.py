class GenericModels(object):
    def models_stub(self, entities):
        """
        $ python -m sagas.feedback_loop.models_generic models_stub Testing,Person
        :param entities:
        :return:
        """
        from sagas.ofbiz.entity_gen import gen_bloc_model
        lines = []
        # entities = ['Testing', 'TestingType', 'TestFieldType', 'Person']
        # entities = ['Person']
        for entity_name in entities:
            # entity_name='TestFieldType'
            gen_bloc_model(lines, entity_name)
        print('\n'.join(lines))

if __name__ == '__main__':
    import fire
    fire.Fire(GenericModels)

