import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.write('Done! (using st.cache)')

"""
当用Streamlit的缓存注释标记一个函数时，它告诉Streamlit每当调用该函数时，它应该检查三件事：
    组成函数主体的实际字节码
    函数依赖的代码，变量和文件
    您用来调用该函数的输入参数
如果这是Streamlit第一次看到具有这些确切值的项目以及这些确切的组合，
它将运行该函数并将结果存储在本地缓存中。下次调用该函数时，如果三个值都没有更改，
则Streamlit知道它可以完全跳过执行该函数。取而代之的是，它从本地缓存中读取输出，
然后像魔术一样将其传递给调用方。

1. Streamlit将仅检查当前工作目录中的更改。
2. 由于缓存的值是按引用存储的（出于性能原因并能够支持TensorFlow之类的库），
因此您不应更改缓存的函数的输出。请注意，在这里，Streamlit足够聪明，
可以检测到这些突变并显示响亮的警告，说明如何解决问题。
3. 只要您的代码中运行了长时间的计算，请考虑对其进行重构，以便可以使用@ st.cache。
"""

# st.write尝试根据输入的数据类型做正确的事情。如果没有按预期执行操作，
# 则可以使用类似的专用命令st.dataframe 。
# st.subheader('Raw data')
# st.write(data)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 绘制直方图
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

"""
在Uber的数据集中使用直方图可以帮助我们确定皮卡最繁忙的时间，
但是如果我们想弄清皮卡在整个城市集中在哪里，那该怎么办。
虽然您可以使用条形图来显示此数据，但是除非您非常熟悉城市中的纬度和经度坐标，
否则就不容易理解。为了显示拾取浓度，让我们使用Streamlit st.map() 函数将数据叠加在纽约市的地图上。
"""

# st.subheader('Map of all pickups')
# st.map(data)

# 用滑块过滤结果; 使用滑块可实时观看地图更新。
# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

'...... .'

