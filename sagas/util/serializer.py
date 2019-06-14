import pickle

def write_data(file, data):
    """
    from sagas.util.serializer import write_data, read_data
    # An arbitrary collection of objects supported by pickle.
    data = {
        'a': [1, 2.0, 3, 4+6j],
        'b': ("character string", b"byte string"),
        'c': {None, True, False}
    }
    write_data('./out/data.pickle', data)

    :param file:
    :param data:
    :return:
    """
    with open(file, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def read_data(file):
    with open(file, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)
        return data

