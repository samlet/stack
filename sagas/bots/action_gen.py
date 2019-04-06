from mako.template import Template
from sagas.util.str_converters import to_camel_case, to_snake_case
import clipboard

"""
python -m sagas.bots.action_gen common about_date
"""

action_def='''
class Action${action_c}(Action):
  def name(self):
    return "action_${action}"

  def run(self, dispatcher, tracker, domain):
    # print(tracker.latest_message)
    dispatcher.utter_message("{}".format('all done.'))
    return [SlotSet("response", 'ok')]
'''

class ActionGen(object):
    def common(self, name):
        mytemplate = Template(action_def)
        # name='about_date'
        result=(mytemplate.render(action=name, action_c=to_camel_case(name, True)))
        print(result)
        clipboard.copy(result)

if __name__ == '__main__':
    import fire
    fire.Fire(ActionGen)
