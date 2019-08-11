# procs-python-itertools.md
⊕ [itertools - 为高效循环创建迭代器的函数 - Python 3.7.3文档](https://docs.python.org/3/library/itertools.html)
    该模块实现了许多迭代器构建块，其灵感来自APL，Haskell和SML的构造。每个都以适合Python的形式重铸。
    该模块标准化了一组核心的快速，内存有效的工具，这些工具本身或组合使用。它们共同组成了一个“迭代器代数”，可以在纯Python中简洁有效地构建专用工具。
    例如，SML提供了一个制表工具：tabulate(f)它产生一个序列。通过组合和形成，可以在Python中实现相同的效果。f(0), f(1), ...map()count()map(f, count())

    这些工具及其内置对应设备也可与operator模块中的高速功能配合使用。例如，乘法运算符可以跨两个向量映射，以形成有效的点积： 。sum(map(operator.mul, vector1, vector2))

    