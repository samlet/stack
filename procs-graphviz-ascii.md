# procs-graphviz-ascii.md
⊕ [Graphviz and ascii output - Stack Overflow](https://stackoverflow.com/questions/3211801/graphviz-and-ascii-output)
⊕ [graph-easy - render/convert graphs in/from various formats - metacpan.org](https://metacpan.org/pod/release/TELS/Graph-Easy-0.64/bin/graph-easy)
⊕ [Graoh Easy 使用介绍 | 大光的博客](https://www.daguang.me/2019/01/11/graph/)
    ⊕ [云风的 BLOG: 用 Ascii 画关系图](https://blog.codingnow.com/2016/12/ascii_graph.html)
        读取任何 label 串时，都把这个串处理一下，把其中的汉字全部追加一个不可能在正常文本中存在的字符 U+FFFF ，让每个汉字都真的占据两个字符位。这样的字符串处理函数原本就在模块内存在（因为它本身就要去做类似 \n 的转义），这样就可以让整个排版过程正常了。
        接下来要改的是最终把 framebuffer 序列化回字符串的过程，把里面所有的 U+FFFF 都删掉，就可以正确的输出了。

## install
```sh
brew install cpanminus
cpan Graph::Easy

# 安装后需要将.bashrc中的PATH变量附加部分复制到.bash_profile里, 因为macos不执行.bashrc.

$ echo "[ Bonn ] -- car --> [ Berlin ], [ Ulm ]" | graph-easy
+--------+  car   +-----+
|  Bonn  | -----> | Ulm |
+--------+        +-----+
  |
  | car
  v
+--------+
| Berlin |
+--------+

$ echo "[ Bonn\nAnd Kite ] -- car --> [ Berlin ], [ Ulm ]" | graph-easy --as_boxart

# or --as_boxart
$ cat dotfile.dot | graph-easy --from=dot --as_ascii

# Graphviz example output
$ echo "[ Bonn ] -- car --> [ Berlin ], [ Ulm ]" | graph-easy --dot
```
