import datetime
import json

import pydgraph

# Create a client stub.
def create_client_stub():
    return pydgraph.DgraphClientStub('localhost:9080')

# Create a client.
def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


# Drop All - discard all data and start from a clean slate.
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))

class GraphManager(object):
    def __init__(self):
        self.client_stub = create_client_stub()
        self.client = create_client(self.client_stub)

    def reset_schema(self, schema):
        drop_all(self.client)
        return self.client.alter(pydgraph.Operation(schema=schema))

    def add_object(self, p):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            # Run mutation.
            assigned = txn.mutate(set_obj=p)

            # Commit transaction.
            txn.commit()
            for uid in assigned.uids:
                print('{} => {}'.format(uid, assigned.uids[uid]))
            return assigned
        finally:
            # Clean up. Calling this after txn.commit() is a no-op
            # and hence safe.
            txn.discard()

    def remove_by_field(self, fld_name, fld_val):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            query1 = """query all($a: string)
            {
               all(func: eq(%s, $a)) 
                {
                   uid
                }   
            }"""%(fld_name)
            variables1 = {'$a': fld_val}
            res1 = self.client.txn(read_only=True).query(query1, variables=variables1)
            ppl1 = json.loads(res1.json)
            for obj in ppl1['all']:
                assigned = txn.mutate(del_obj=obj)
                for uid in assigned.uids:
                    print('remove: {} => {}'.format(uid, assigned.uids[uid]))

            txn.commit()

        finally:
            txn.discard()

    def query(self, query, variables=None):
        res = self.client.txn(read_only=True).query(query, variables=variables)
        rs = json.loads(res.json)
        return rs

class GraphCommander(object):
    def __init__(self):
        self.gm= GraphManager()

    def create_schema_stuff(self):
        schema = """
            name: string @index(exact) .
            friend: uid @reverse .
            age: int .
            married: bool .
            loc: geo .
            dob: datetime .
            """
        self.gm.reset_schema(schema)

    def create_data_stuff(self):
        # Create data.
        p = {
            'name': 'Alice',
            'age': 26,
            'married': True,
            'loc': {
                'type': 'Point',
                'coordinates': [1.1, 2],
            },
            'dob': datetime.datetime(1980, 1, 1, 23, 0, 0, 0).isoformat(),
            'friend': [
                {
                    'name': 'Bob',
                    'age': 24,
                },
                {
                    'name': 'Charlie',
                    'age': 29,
                }
            ],
            'school': [
                {
                    'name': 'Crown Public School',
                }
            ]
        }
        self.gm.add_object(p)

    def create_and_query_stuff(self):
        """
        $ python -m sagas.graph.graph_manager create-and-query-stuff
        :return:
        """
        self.create_schema_stuff()
        self.create_data_stuff()

        query = """{
          find_person(func: eq(name, "Alice")) {
            uid
            name
            age
          }
        }
        """
        rs=self.gm.query(query)
        print(json.dumps(rs, indent=True))

if __name__ == '__main__':
    import fire
    fire.Fire(GraphCommander)
