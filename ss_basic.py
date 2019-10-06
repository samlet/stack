import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy
import pandas
import time

st.title('My first app')

# st.write()是Streamlit的“瑞士军刀”。您几乎可以将任何内容传递给st.write()：
# 文本，数据，Matplotlib图形，Altair图表等等。
st.write("Here's our first attempt at using data to create a table:")
st.write(pandas.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# 使用Numpy生成一个随机样本，然后将其绘制成图表。
chart_data = pandas.DataFrame(
     numpy.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# 使用st.map()可以在地图上显示数据点。让我们使用Numpy生成一些样本数据并将其绘制在旧金山地图上。
map_data = pandas.DataFrame(
    numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

# 复选框的一个用例是隐藏或显示应用程序中的特定图表或部分。
# st.checkbox()接受一个参数，即小部件标签。在此示例中，该复选框用于切换条件语句。
if st.checkbox('Show dataframe'):
    chart_data = pandas.DataFrame(
       numpy.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

df = pandas.DataFrame({
    'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40]
    })

df

# 使用选择框作为选项:
#   用于st.selectbox从系列中选择。您可以编写所需的选项，也可以通过数组或数据框列。
#   让我们使用df之前创建的数据框。
option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

# 为了使外观更整洁，可以将小部件移动到侧边栏中。这将您的应用保持在中心位置，而小部件固定在左侧。
# 让我们看一下如何st.sidebar()在应用程序中使用：

option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected:', option

# 您可以通过st.something()调用将大部分元素放入应用的主要部分，
# 也可以使用放到侧边栏中 st.sidebar.something()。
# 现在唯一的例外是st.write（和应该使用st.sidebar.markdown()）st.echo，和st.spinner。

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'


