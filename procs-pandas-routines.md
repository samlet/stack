# procs-pandas-routines.md
⊕ [pandas.Period — pandas 0.24.1 documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html?highlight=period)
    day Get day of the month that a Period falls on.
    dayofweek   Day of the week the period lies in, with Monday=0 and Sunday=6.
    dayofyear   Return the day of the year.
    days_in_month   Get the total number of days in the month that this period falls on.
    daysinmonth Get the total number of days of the month that the Period falls in.
    hour    Get the hour of the day component of the Period.
    minute  Get minute of the hour component of the Period.
    qyear   Fiscal year the Period lies in according to its starting-quarter.
    second  Get the second component of the Period.
    start_time  Get the Timestamp for the start of the period.
    week    Get the week of the year on the given Period.
    weekday Day of the week the period lies in, with Monday=0 and Sunday=6.

+ jcloud/assets/langs/workspace/arrow/procs-pandas.md

## start
```python
import numpy as np
import pandas as pd
import pyarrow as pa

np.random.seed(1234)
d1 = pd.Series(2*np.random.normal(size = 100)+3)
d2 = np.random.f(2,4,size = 100)
d3 = np.random.randint(1,100,size = 100)

# 在0-7中随机产生10个整数
s = pd.Series(np.random.randint(0, 7, size=10))
# 对数据进行计数
s.value_counts()
# 创建一个Series
s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat']) 

# ⊕ [python dataframe pandas drop column using int - Stack Overflow](https://stackoverflow.com/questions/20297317/python-dataframe-pandas-drop-column-using-int)

# You can delete column on i index like this:
df.drop(df.columns[i], axis=1)

# It could work strange, if you have duplicate names in columns, so to do this you can rename column you want to delete column by new name. Or you can reassign DataFrame like this:

df = df.iloc[:, [j for j, c in enumerate(df.columns) if j != i]]

# Drop multiple columns like this:

cols = [1,2,4,5,12]
df.drop(df.columns[cols],axis=1,inplace=True)
```

## read
⊕ [Pandas Tutorial 1: Pandas Basics (read_csv, DataFrame, Data Selection)](https://data36.com/pandas-tutorial-1-basics-reading-data-files-dataframes-data-selection/)

```python
article_read = pd.read_csv('pandas_tutorial_read.csv', delimiter=';', names = ['my_datetime', 'event', 'country', 'user_id', 'source', 'topic'])

pd.read_csv('zoo.csv', delimiter = ',')

# read .tab
df=pd.read_csv('/pi/ai/nltk/data/wikt/wn-wikt-rus.tab',sep='\t')
```

## modify columns
⊕ [python - Pandas: how to change all the values of a column? - Stack Overflow](https://stackoverflow.com/questions/12604909/pandas-how-to-change-all-the-values-of-a-column)

```python
df['Date'].str[-4:].astype(int)
# Or using extract (assuming there is only one set of digits of length 4 somewhere in each string):
df['Date'].str.extract('(?P<year>\d{4})').astype(int)

# An alternative slightly more flexible way, might be to use apply (or equivalently map) to do this:

df['Date'] = df['Date'].apply(lambda x: int(str(x)[-4:]))
             #  converts the last 4 characters of the string to an integer

# The lambda function, is taking the input from the Date and converting it to a year.
# You could (and perhaps should) write this more verbosely as:

def convert_to_year(date_in_some_format);
    date_as_string = str(date_in_some_format)
    year_as_string = date_in_some_format[-4:] # last four characters
    return int(year_as_string)

df['Date'] = df['Date'].apply(convert_to_year)

## ... my practice
df['children'] = df['children'].apply(lambda x: ', '.join(x)[:20] + "..")
```

## remove columns
⊕ [python - Delete column from pandas DataFrame - Stack Overflow](https://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe)

```python
# The best way to do this in pandas is to use drop:
df = df.drop('column_name', 1)
# where 1 is the axis number (0 for rows and 1 for columns.)

# To delete the column without having to reassign df you can do:
df.drop('column_name', axis=1, inplace=True)

# Finally, to drop by column number instead of by column label, try this to delete, e.g. the 1st, 2nd and 4th columns:
df = df.drop(df.columns[[0, 1, 3]], axis=1)  # df.columns is zero-based pd.Index 

# This will delete one or more columns in-place.
columns = ['Col1', 'Col2', ...]
df.drop(columns, inplace=True, axis=1)
```

## string
⊕ [python - Ignoring NaNs with str.contains - Stack Overflow](https://stackoverflow.com/questions/28311655/ignoring-nans-with-str-contains)
⊕ [Pandas: Select rows that match a string - David Hamann](https://davidhamann.de/2017/06/26/pandas-select-elements-by-string/)

```python
In [11]: df = pd.DataFrame([["foo1"], ["foo2"], ["bar"], [np.nan]], columns=['a'])
In [12]: df.a.str.contains("foo")
In [13]: df.a.str.contains("foo", na=False)

df[df['Product ID'].str.contains("foo") == True]

# Select rows that match a string
import pandas as pd

#create sample data
data = {'model': ['Lisa', 'Lisa 2', 'Macintosh 128K', 'Macintosh 512K'],
        'launched': [1983,1984,1984,1984],
        'discontinued': [1986, 1985, 1984, 1986]}

df = pd.DataFrame(data, columns = ['model', 'launched', 'discontinued'])
df
# We want to select all rows where the column ‘model’ starts with the string ‘Mac’.
df[df['model'].str.match('Mac')]
df[df['model'].str.contains('ac')]
# More info about working with text data: https://pandas.pydata.org/pandas-docs/stable/text.html
```

## date-time
```python
# 创建了一个100秒时间戳的系列，s为second的意思
rng = pd.date_range('1/1/2012', periods=100, freq='S')
# 将刚产生的时间序列rng作为索引index，随机产生0-500之间的整数作为值。
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
# 将该系列缩小为5分钟,就是五分钟采样一次，并对其值进行求和：
ts.resample('5Min').sum()
```

## iterate
```python
for item, frame in df['Column2'].iteritems():
    if pd.notnull(frame):
        print frame

import pandas as pd
import numpy as np

df = pd.DataFrame([{'c1':10, 'c2':100}, {'c1':11,'c2':110}, {'c1':12,'c2':120}])
for index, row in df.iterrows():
    print(row['c1'], row['c2'])
# Output: 
#    10 100
#    11 110
#    12 120 

# Use DataFrame.apply() instead:
new_df = df.apply(lambda x: x * 2)

#⊕ [pandas.DataFrame.apply — pandas 0.24.2 documentation](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html)
>>> df = pd.DataFrame([[4, 9],] * 3, columns=['A', 'B'])
>>> df
   A  B
0  4  9
1  4  9
2  4  9
# Using a numpy universal function (in this case the same as np.sqrt(df)):
>>> df.apply(np.sqrt)
     A    B
0  2.0  3.0
1  2.0  3.0
2  2.0  3.0
# Using a reducing function on either axis
>>> df.apply(np.sum, axis=0)
A    12
B    27
dtype: int64
>>> df.apply(np.sum, axis=1)
0    13
1    13
2    13
dtype: int64
```

## checkers
```python
# give you the data for which Column2 has not null value
df[df['Column2'].notnull()]
```

## merge
```python
new_df = pd.merge(A_df, B_df,  how='left', left_on=['A_c1','c2'], right_on = ['B_c1','c2'])
# http://pandas.pydata.org/pandas-docs/version/0.19.1/generated/pandas.DataFrame.merge.html
```
left_on : label or list, or array-like Field names to join on in left DataFrame. Can be a vector or list of vectors of the length of the DataFrame to use a particular vector as the join key instead of columns

right_on : label or list, or array-like Field names to join on in right DataFrame or vector/list of vectors per left_on docs

⊕ [Python: pandas merge multiple dataframes - Stack Overflow](https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes)

```python
# Just simply merge with DATE as the index and merge using OUTER method (to get all the data).

import pandas as pd
from functools import reduce

df1 = pd.read_table('file1.csv', sep=',')
df2 = pd.read_table('file2.csv', sep=',')
df3 = pd.read_table('file3.csv', sep=',')

# So, basically load all the files you have as data frame. Then merge the files using merge or reduce function.

# compile the list of dataframes you want to merge
data_frames = [df1, df2, df3]

# you can add as many data-frames in the above code. This is the good part about this method. No complex queries involved.

# To keep the values that belong to the same date you need to merge it on the DATE

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['DATE'],
                                            how='outer'), data_frames)

# if you want to fill the values that don't exist in the lines of merged dataframe simply fill with required strings as

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['DATE'],
                                            how='outer'), data_frames).fillna('void')

# So, the values from the same date are on the same lines.
# You can fill the non existing data from different frames for different columns using fillna().
# Then write the merged data to the csv file if desired.

pd.DataFrame.to_csv(df_merged, 'merged.txt', sep=',', na_rep='.', index=False)
# This should give you result.
```

