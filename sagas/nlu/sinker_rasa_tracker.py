from typing import Text, Any, Dict, List, Union

from rasa.core.events import (
    SlotSet,
    ActionExecuted,
    Restarted,
    UserUttered,
    SessionStarted,
    BotUttered,
    Event,
)
from rasa.core.trackers import DialogueStateTracker
from rasa.core.domain import Domain
from sagas.conf.conf import cf
from sagas.nlu.sinker_intf import SinkerStoreIntf


def get_default_domain():
    content = """
    actions:
      - utter_hello

    intents:
      - greet
      - bye
      - affirm
      - deny
    entities:
      - object_type
      - mention
      - attribute
      - sents

    slots:
      attribute:
        type: unfeaturized
      mention:
        type: unfeaturized
      object:
        type: unfeaturized
      object_type:
        type: unfeaturized
      parameters:
        type: unfeaturized
      sents:
        type: unfeaturized
      from:
        type: unfeaturized
      to:
        type: unfeaturized
      transport_cat:
        type: unfeaturized
      transport_name:
        type: unfeaturized

    session_config:
        session_expiration_time: 60
        carry_over_slots_to_new_session: true
    """
    return Domain.from_yaml(content)

bucket_id=lambda h_id, user=None: f"{cf.user}_{h_id}" if user is None else f"{user}_{h_id}"
class RasaTrackerStore(SinkerStoreIntf):
    def __init__(self):
        from rasa.core.tracker_store import (
            TrackerStore,
            InMemoryTrackerStore,
            MongoTrackerStore)
        default_domain = get_default_domain()
        self.tracker_store = MongoTrackerStore(domain=default_domain)

    def drop(self):
        self.tracker_store.conversations.drop()

    def store(self, bucket: Text, values: Dict[Text, Any], user=None):
        evts=[]
        tracker = self.tracker_store.get_or_create_tracker(bucket_id(bucket, user))
        for slot_key, slot_val in values.items():
            evts.append(SlotSet(slot_key, slot_val))
        for e in evts:
            tracker.update(e)
        self.tracker_store.save(tracker)


    def get_bucket(self, bucket:Text, user=None):
        tracker = self.tracker_store.get_or_create_tracker(bucket_id(bucket, user))
        # tracker.events
        dialogue = tracker.as_dialogue()
        return dialogue.as_dict()

    def slot_values(self, bucket:Text, user=None):
        tracker = self.tracker_store.get_or_create_tracker(bucket_id(bucket, user))
        return tracker.current_slot_values()

rasa_tracker_store=RasaTrackerStore()

class TrackerCli(object):
    def slots(self, bucket:Text, user=None):
        """
        $ preqs: launch sagas-ai/bots/agent_dispatcher/Procfile_mod
        $ saai talk '/dump_info{"object":"rr"}' samlet_default
        $ python -m sagas.nlu.sinker_rasa_tracker slots default

        $ sj '新幹線で東京から大阪まで行きました。'
        $ python -m sagas.nlu.sinker_rasa_tracker slots transport
        :param bucket:
        :param user:
        :return:
        """
        import sagas.tracker_fn as tc
        values=rasa_tracker_store.slot_values(bucket, user)
        tc.emp('green', [f"{k}: {v}" for k,v in values.items() if v is not None])

if __name__ == '__main__':
    import fire
    fire.Fire(TrackerCli)

