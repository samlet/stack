import pandas as pd

def to_df(list_of_tuples, columns):
    """
    import sagas.util.pandas_helper as ph
    ph.to_df(tuples, ['title', 'published', 'id'])
    :param list_of_tuples:
    :param columns:
    :return:
    """
    return pd.DataFrame(list_of_tuples, columns=columns)

class PandasData(object):
    def __init__(self, columns):
        self.columns=columns

    def to_df(self, *iterators):
        mapped = zip(*iterators)
        df = pd.DataFrame(list(mapped), columns = self.columns)
        return df

"""
procs-pandas-and-collections.ipynb
"""
class PandasHelper(object):
    def tests(self):
        columns = ['name', 'roll', 'marks']
        data=PandasData(columns)
        # initializing lists
        name = ["Manjeet", "Nikhil", "Shambhavi", "Astha"]
        roll_no = [4, 1, 3, 2]
        marks = [40, 50, 60, 70]
        df=data.to_df(name, roll_no, marks)
        print(df)

if __name__ == '__main__':
    import fire
    fire.Fire(PandasHelper)
