# procs-form.md
## extract slots
1. 在extract的过程中, 对于非当前requested_slot的slots, 只会提取同名的实体, 并不会完全执行slot_mappings里的定义. 这其中主要原因应该是tracker里的intent只是相对当前的requested_slot而言的, 所以做全面提取容易混淆.

+ 下面这个代码, 由于requested_slot是outdoor_seating, 所以并不会将('entity': 'number')提取到num_people实体里, 所以执行的结果会是[{'template': 'utter_ask_num_people'}], 而如果requested_slot是num_people的话, 则会提取number实体到num_people中, 但不会提取outdoor_seating; 返回的slots事件会让tracker在调用端固化实体值到slots中, 这样下次就不需要再提取了.

```python
import logging
import sys
from utils import dump

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.DEBUG, stream=sys.stdout)

form = RestaurantForm()

tracker = Tracker('default', {'requested_slot': 'outdoor_seating'},
                  {'intent': {'name': 'inform',
                                  'confidence': 1.0},
                   'entities': [{'entity': 'cuisine',
                                 'value': 'chinese'},
                                {'entity': 'number',
                                 'value': '8'},
                                {'entity': 'feedback',
                                 'value': 'its good'},
                                {'entity': 'seating',
                                 'value': 'in'},
                                {'entity': 'some_other_slot',
                                 'value': 'some_other_value'}]
                    },
                  [], False, None, 
                  {'name': 'restaurant_form',
                       'validate': True, 'rejected': False},
                  'action_listen')
print("✁ req", tracker.slots, tracker.latest_message)

dispatcher=CollectingDispatcher()
domain=Domain.load(DOMAIN_PATH)
events=form.run(dispatcher, tracker, domain)
for ev in events:
    print(str(ev))
print("☈", dispatcher.messages)
print(form.required_slots(tracker))
```

