# procs-python-module.md
⊕ [Python导入模块的几种姿势| 编程派 | Coding Python](http://codingpy.com/article/python-import-101/)

如果你往module_x.py文件中添加了if __name__ == ‘__main__’，然后试图运行这个文件，你会碰到一个很难理解的错误。编辑一下文件，试试看吧！

```python
from . module_y import spam as ham

def main():
    ham()

if __name__ == '__main__':
    # This won't work!
    main()
```
现在从终端进入subpackage1文件夹，执行以下命令：

python module_x.py

如果你使用的是Python 2，你应该会看到下面的错误信息：

Traceback (most recent call last):
  File "module_x.py", line 1, in <module>
    from . module_y import spam as ham
ValueError: Attempted relative import in non-package

如果你使用的是Python 3，错误信息大概是这样的：

Traceback (most recent call last):
  File "module_x.py", line 1, in <module>
    from . module_y import spam as ham
SystemError: Parent module '' not loaded, cannot perform relative import
这指的是，module_x.py是某个包中的一个模块，而你试图以脚本模式执行，但是这种模式不支持相对导入。

如果你想在自己的代码中使用这个模块，那么你必须将其添加至Python的导入检索路径（import search path）。最简单的做法如下：

import sys
sys.path.append('/path/to/folder/containing/my_package')
import my_package
注意，你需要添加的是my_package的上一层文件夹路径，而不是my_package本身。原因是my_package就是我们想要使用的包，所以如果你添加它的路径，那么将无法使用这个包。

