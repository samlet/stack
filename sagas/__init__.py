from sagas.util.pandas_helper import to_df, dict_df
from sagas.util.name_util import to_global_id, from_global_id
# from sagas.nlu.corenlp_helper import LangDialect as dia
from sagas.util.collection_util import *
# import sagas.nlu.locales as locales

def print_df(df):
    from tabulate import tabulate
    # import pandas as pd
    # pd.set_option('display.unicode.ambiguous_as_wide', True)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def print_rs(rs, cols):
    print_df(to_df(rs, cols))

def runtime_dir():
    import os
    return os.path.dirname(__file__)
