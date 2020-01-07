import requests
from pprint import pprint

def a_joke():
    request = requests.get('http://api.icndb.com/jokes/random').json()  # make an api call
    joke = request['value']['joke']  # extract a joke from returned json response
    # dispatcher.utter_message(joke)  # send the message back to the user
    return joke

def rs_users():
    # randomuser.me generates random 'user' data (name, email, addr, phone number, etc)
    r = requests.get('http://api.randomuser.me/0.6/?nat=us&results=10')
    j = r.json()['results']
    return j

stuff_mapping={'joke': a_joke,
               'users': rs_users,
               }

class StuffData(object):
    def request_stuff(self, name):
        """
        $ python -m sagas.dataset.stuff_data request_stuff joke

        :param name:
        :return:
        """
        if name in stuff_mapping:
            return stuff_mapping[name]()
        return ''

    def print_rs(self, name):
        """
        $ python -m sagas.dataset.stuff_data print_rs users
        :param name:
        :return:
        """
        for el in stuff_mapping[name]():
            pprint(el)

stuff_data=StuffData()

if __name__ == '__main__':
    import fire
    fire.Fire(StuffData)



