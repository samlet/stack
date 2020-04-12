import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy import create_engine
from pprint import pprint
import os

# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine("mysql://dev:dev@samlet/bot?charset=utf8mb4", echo=True)
# engine = create_engine("mysql://dev:dev@samlet/bot?charset=utf8mb4&&use_unicode=True", echo=False)

# preqs: pip install PyMySQL
# engine = create_engine("mysql+pymysql://dev:dev@samlet/bot?charset=utf8mb4&&use_unicode=True", echo=False)
# db_host=os.getenv('db_host') or 'samlet'
# engine = create_engine(f"mysql+pymysql://dev:dev@{db_host}/bot?charset=utf8mb4&&use_unicode=True", echo=False)

engine = create_engine("mysql+pymysql://root:root@localhost/bot?charset=utf8mb4&&use_unicode=True", echo=False)

metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=50)),
    Column('fullname', String(length=50)),
)

addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('email_address', String(length=50), nullable=False)
 )

restaurant = Table('restaurant', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=100)),
    Column('cuisine', String(length=50)),
    Column('price_range', String(length=50)),
    Column('outside_seating', Boolean),
)

hotel = Table('hotel', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=100)),
    Column('city', String(length=50)),
    Column('price_range', String(length=50)),
    Column('breakfast_included', Boolean),
    Column('free_wifi', Boolean),
    Column('swimming_pool', Boolean),
    Column('star_rating', Integer),
)

class DataSource(object):
    def setup(self):
        metadata.drop_all(engine)  # drop all tables
        metadata.create_all(engine)

    def fill_stuffs(self):
        conn = engine.connect()

        ins = users.insert()
        conn.execute(ins, id=1, name='jack', fullname='Jack')
        conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')

        conn.execute(addresses.insert(), [
            {'user_id': 1, 'email_address': 'jack@yahoo.com'},
            {'user_id': 1, 'email_address': 'jack@msn.com'},
            {'user_id': 2, 'email_address': 'www@www.org'},
            {'user_id': 2, 'email_address': 'wendy@aol.com'},
        ])

    def query_stuffs(self):
        from sqlalchemy.sql import select

        conn = engine.connect()
        s = select([users.c.name, users.c.fullname])
        result = conn.execute(s)
        for row in result:
            print(row)

    def initial_table(self, metacls, table_data):
        conn = engine.connect()
        recs = []
        for rec in table_data:
            recs.append({k.replace('-', '_'): v for k, v in rec.items() if k != 'id'})

        pprint(recs)
        conn.execute(metacls.insert(), recs)

    def fill_data_seeds(self, recreate=False):
        """
        $ python -m sagas.modules.life.data_source fill_data_seeds
        $ python -m sagas.modules.life.data_source fill_data_seeds True  # recreate tables

        :return:
        """
        import json_utils
        import pkg_resources

        if recreate:
            self.setup()

        path=pkg_resources.resource_filename(__name__, 'knowledge_base_data.json')
        dataset = json_utils.read_json_file(path)
        print(dataset.keys())
        # fill dataset
        self.initial_table(restaurant, dataset['restaurant'])
        self.initial_table(hotel, dataset['hotel'])

    def dev_stack(self):
        """
        $ python -m sagas.modules.life.data_source dev_stack

        :return:
        """
        self.setup()
        self.fill_stuffs()
        self.query_stuffs()

    def browse(self, table_name, as_json=False):
        """
        $ python -m sagas.modules.life.data_source browse hotel
        $ python -m sagas.modules.life.data_source browse restaurant True
        :param table_name:
        :return:
        """
        import pandas as pd
        import json

        query = f"select * from {table_name}"
        df = pd.read_sql_query(query, engine)
        if as_json:
            recs=json.loads(df.to_json(orient='records'))
            pprint(recs)
        else:
            print(df)

if __name__ == '__main__':
    import fire
    fire.Fire(DataSource)


