# procs-python-date-time.md
⊕ [Converting Strings To Datetime](https://chrisalbon.com/python/basics/strings_to_datetime/)
⊕ [Python DateTime, TimeDelta, Strftime(Format) with Examples](https://www.guru99.com/date-time-and-datetime-classes-in-python.html)
⊕ [datetime — Basic date and time types — Python 3.7.4 documentation](https://docs.python.org/3/library/datetime.html)

## dateparser
```sh
$ pip install convertdate
$ pip install dateparser
```
```python
>>> from dateparser.calendars.jalali import JalaliCalendar
>>> JalaliCalendar(u'جمعه سی ام اسفند ۱۳۸۷').get_date()
{'date_obj': datetime.datetime(2009, 3, 20, 0, 0), 'period': 'day'}
```

## start
```python
from dateutil.parser import parse
print(entry.published)
print(parse(entry.published).isoformat())
```
```python
from datetime import datetime
from dateutil.parser import parse
import pandas as pd

# Create a string variable with the war start time
war_start = '2011-01-03'
# Convert the string to datetime format
datetime.strptime(war_start, '%Y-%m-%d')
datetime.datetime(2011, 1, 3, 0, 0)
# Create a list of strings as dates
attack_dates = ['7/2/2011', '8/6/2012', '11/13/2013', '5/26/2011', '5/2/2001']
# Convert attack_dates strings into datetime format
[datetime.strptime(x, '%m/%d/%Y') for x in attack_dates]
♮   [datetime.datetime(2011, 7, 2, 0, 0),
     datetime.datetime(2012, 8, 6, 0, 0),
     datetime.datetime(2013, 11, 13, 0, 0),
     datetime.datetime(2011, 5, 26, 0, 0),
     datetime.datetime(2001, 5, 2, 0, 0)]
# Use parse() to attempt to auto-convert common string formats
parse(war_start)
datetime.datetime(2011, 1, 3, 0, 0)
# Use parse() on every element of the attack_dates string
[parse(x) for x in attack_dates]
♮   [datetime.datetime(2011, 7, 2, 0, 0),
     datetime.datetime(2012, 8, 6, 0, 0),
     datetime.datetime(2013, 11, 13, 0, 0),
     datetime.datetime(2011, 5, 26, 0, 0),
     datetime.datetime(2001, 5, 2, 0, 0)]
# Use parse, but designate that the day is first
parse(war_start, dayfirst=True)
datetime.datetime(2011, 3, 1, 0, 0)
# Create a dataframe
data = {'date': ['2014-05-01 18:47:05.069722', '2014-05-01 18:47:05.119994', '2014-05-02 18:47:05.178768', '2014-05-02 18:47:05.230071', '2014-05-02 18:47:05.230071', '2014-05-02 18:47:05.280592', '2014-05-03 18:47:05.332662', '2014-05-03 18:47:05.385109', '2014-05-04 18:47:05.436523', '2014-05-04 18:47:05.486877'], 
        'value': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
df = pd.DataFrame(data, columns = ['date', 'value'])
print(df)
                         date  value
0  2014-05-01 18:47:05.069722      1
1  2014-05-01 18:47:05.119994      1
2  2014-05-02 18:47:05.178768      1
3  2014-05-02 18:47:05.230071      1
4  2014-05-02 18:47:05.230071      1
5  2014-05-02 18:47:05.280592      1
6  2014-05-03 18:47:05.332662      1
7  2014-05-03 18:47:05.385109      1
8  2014-05-04 18:47:05.436523      1
9  2014-05-04 18:47:05.486877      1
# Convert df['date'] from string to datetime
pd.to_datetime(df['date'])
0   2014-05-01 18:47:05.069722
1   2014-05-01 18:47:05.119994
2   2014-05-02 18:47:05.178768
3   2014-05-02 18:47:05.230071
4   2014-05-02 18:47:05.230071
5   2014-05-02 18:47:05.280592
6   2014-05-03 18:47:05.332662
7   2014-05-03 18:47:05.385109
8   2014-05-04 18:47:05.436523
9   2014-05-04 18:47:05.486877
Name: date, dtype: datetime64[ns]
```

## datetime.isoformat(sep='T', timespec='auto')
Return a string representing the date and time in ISO 8601 format, YYYY-MM-DDTHH:MM:SS.ffffff or, if microsecond is 0, YYYY-MM-DDTHH:MM:SS

If utcoffset() does not return None, a string is appended, giving the UTC offset: YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM[:SS[.ffffff]] or, if microsecond is 0 YYYY-MM-DDTHH:MM:SS+HH:MM[:SS[.ffffff]].

The optional argument sep (default 'T') is a one-character separator, placed between the date and time portions of the result. For example,

```python
>>> from datetime import tzinfo, timedelta, datetime
>>> class TZ(tzinfo):
...     def utcoffset(self, dt): return timedelta(minutes=-399)
...
>>> datetime(2002, 12, 25, tzinfo=TZ()).isoformat(' ')
'2002-12-25 00:00:00-06:39'
```
The optional argument timespec specifies the number of additional components of the time to include (the default is 'auto'). It can be one of the following:

     'auto': Same as 'seconds' if microsecond is 0, same as 'microseconds' otherwise.

     'hours': Include the hour in the two-digit HH format.

     'minutes': Include hour and minute in HH:MM format.

     'seconds': Include hour, minute, and second in HH:MM:SS format.

     'milliseconds': Include full time, but truncate fractional second part to milliseconds. HH:MM:SS.sss format.

     'microseconds': Include full time in HH:MM:SS.ffffff format.


