def simple():
    from pymongo import MongoClient
    import sagas

    # uri = 'mongodb://samlet.com/langs'
    uri = 'mongodb://localhost/langs'
    # uri = 'mongodb://192.168.0.101/langs'
    client = MongoClient(uri)
    db = client.get_default_database()
    print(db.name)

    rs = []
    for r in db.trans.find({'source': 'id'}):
        rs.append((r['text'], r['target']))
    sagas.print_df(sagas.to_df(rs, ['text', 'target']))

if __name__ == '__main__':
    simple()
