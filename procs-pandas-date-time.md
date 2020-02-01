# procs-pandas-date-time.md
⊕ [Select Pandas dataframe rows between two dates | Data Interview Questions](https://www.interviewqs.com/ddi_code_snippets/select_pandas_dataframe_rows_between_two_dates)

## start
```python
import pandas as pd
import numpy as np
# create dummy dataframe
raw_data = {'name': ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'],
'age': [20, 19, 22, 21],
'favorite_color': ['blue', 'red', 'yellow', "green"],
'grade': [88, 92, 95, 70],
'birth_date': ['01-02-1996', '08-05-1997', '04-28-1996', '12-16-1995']}
df = pd.DataFrame(raw_data, index = ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'])
df

df['birth_date'] = pd.to_datetime(df['birth_date'])

# next, set the desired start date and end date to filter df with
# -- these can be in datetime (numpy and pandas), timestamp, or string format

start_date = '03-01-1996'
end_date = '06-01-1997'

# next, set the mask -- we can then apply this to the df to filter it

mask = (df['birth_date'] > start_date) & (df['birth_date'] <= end_date)

# assign mask to df to return the rows with birth_date between our specified start/end dates

df = df.loc[mask]
df
```


