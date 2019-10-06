# procs-python-profiler.md
⊕ [The Python Profilers — Python 3.7.4 documentation](https://docs.python.org/3/library/profile.html#instant-user-s-manual)
    python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)
⊕ [SnakeViz](https://jiffyclub.github.io/snakeviz/#starting-snakeviz)
    SnakeViz is a browser based graphical viewer for the output of Python’s cProfile module and an alternative to using the standard library pstats module. It was originally inspired by RunSnakeRun. SnakeViz works on Python 2.7 and Python 3. SnakeViz itself is still likely to work on Python 2.6, but official support has been dropped now that Tornado no longer supports Python 2.6.
    
## start
+ 在python3.7下才可以支持命令行上的模块调用测试.

```sh
$ using rasa_1x
$ python -m cProfile -o ./out/program.prof -m sagas.ja.knp_cli parse "望遠鏡で泳いでいる少女を見た。"

$ pip install snakeviz
$ snakeviz out/program.prof
# 显示web页面供分析用.
```

