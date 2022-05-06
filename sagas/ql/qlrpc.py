from gql import Client, gql
from sagas.ql.connector import QlConnector
from sagas.misc.utils import *

class QlRpc(object):
    def __init__(self):
        self.qlc=QlConnector()

    def list_people(self):
        """
        $ python -m sagas.ql.qlrpc list_people
        :return:
        """
        result = self.qlc.execute('''
            {
                party {
                    listPeople {
                        id
                        party {
                            party_type_id
                        }
                    }
                }
            }
        ''')
        rs = [e for e in result['party']['listPeople']]
        pp.pprint(rs)

    def entity(self, ent):
        """
        $ python -m sagas.ql.qlrpc entity PartyNote
        :param ent:
        :return:
        """
        result=self.qlc.client.execute(gql('''
            query GetModel($ent: String){
              model {
                    entity(name: $ent) {
                        name
                        combine
                        keys {value}
                        fields {
                            value {
                                name
                                type
                                pk
                            }
                        }
                        relations {
                            value {
                                name
                                relEntityName
                                keymaps {key value}
                            }
                        }
                    }
                }
            }
            '''), variable_values={"ent": ent})
        pp.pprint(result['model']['entity'])

if __name__ == '__main__':
    import fire
    fire.Fire(QlRpc)


