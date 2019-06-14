import pydgraph
import json

SERVER_ADDR = 'localhost:9080'

def create_client(addr=SERVER_ADDR):
    """Creates a new client object using the given address."""
    return pydgraph.DgraphClient(pydgraph.DgraphClientStub(addr))


def set_schema(client, schema):
    """Sets the schema in the given client."""
    return client.alter(pydgraph.Operation(schema=schema))


def drop_all(client):
    """Drops all data in the given client."""
    return client.alter(pydgraph.Operation(drop_all=True))


def setup():
    """Creates a new client and drops all existing data."""
    client = create_client()
    drop_all(client)
    return client

def reset(schema):
    """
    Usage:
    import sagas.graph.dgraph_helper as helper
    import pydgraph
    client=helper.reset('name: string @index(term) .')

    :param schema:
    :return:
    """
    client = create_client()
    # client.login("root", "password")
    drop_all(client)
    set_schema(client, schema)
    return client

def set_nquads(client, nquads):
    '''
    set_nquads(client, """
		_:person1 <name> "Daniel" (वंश="स्पेनी", ancestry="Español") .
		_:person2 <name> "Raj" (वंश="हिंदी", ancestry="हिंदी") .
		_:person3 <name> "Zhang Wei" (वंश="चीनी", ancestry="中文") .
    """)
    :param client:
    :param nquads:
    :return:
    '''
    txn = client.txn()
    return txn.mutate(pydgraph.Mutation(commit_now=True), set_nquads=nquads)

def set_json(client, val):
    """
    _=set_json(client, feed_json)
    :param client:
    :param val:
    :return:
    """
    txn = client.txn()
    return txn.mutate(pydgraph.Mutation(commit_now=True), set_obj=val)

def print_rs(response):
    rs=json.loads(response.json)
    print(json.dumps(rs, ensure_ascii=False, indent=2))

def run_q(client, query):
    """
    run_q(client, '''{
      data(func: eq(name, "Alice")) {
        name
        friend @facets {
          name
          car @facets
        }
      }
    }
    ''')
    :param client:
    :param query:
    :return:
    """
    response = client.txn().query(query)
    print_rs(response)

def query_with_vars(client, query, vars):
    """
    vars = {'$a': 'on a diet'}
    query_with_vars(client, '''query data($a: string){
      data(func: alloftext(sents, $a)) {
         sents
         ja
      }
    }''', vars)

    :param client:
    :param query:
    :param vars:
    :return:
    """
    response = client.txn().query(query, variables=vars)
    print_rs(response)

'''
Extends the base class:

class TestQueries(GraphBase):
    """Tests behavior of queries after mutation in the same transaction."""

    def connect(self):
        super(TestQueries, self).connect()

        helper.drop_all(self.client)
        helper.set_schema(self.client, 'name: string @index(term) .')
'''
class GraphBase(object):
    def connect(self, addr=SERVER_ADDR):
        """Sets up the client."""
        self.client = create_client(addr)
        # self.client.login("groot", "password")
