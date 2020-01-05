import questionary

class QuestionaryTool(object):
    def simple(self):
        """
        $ python -m sagas.tests.cli.questionary_tool simple
        :return:
        """
        questionary.select(
            "What do you want to do?",
            choices=[
                'Order a pizza',
                'Make a reservation',
                'Ask for opening hours'
            ]).ask()  # returns value of selection

if __name__ == '__main__':
    import fire
    fire.Fire(QuestionaryTool)


