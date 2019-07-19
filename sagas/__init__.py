from sagas.util.pandas_helper import to_df
from sagas.util.name_util import to_global_id, from_global_id

def print_df(df):
    from tabulate import tabulate
    # import pandas as pd
    # pd.set_option('display.unicode.ambiguous_as_wide', True)
    print(tabulate(df, headers='keys', tablefmt='psql'))

