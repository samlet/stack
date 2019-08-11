# procs-rocksdb.md
⊕ [Leveldb/Rocksdb/Accumulo简单比较 - 简书](https://www.jianshu.com/p/4c57cd82ccde)
    Rocksdb其实是Leveldb的改进版，RocksDB支持一次获取多个K-V，还支持Key范围查找。LevelDB只能获取单个Key,RocksDB除了简单的Put、Delete操作，还提供了一个Merge操作，说是为了对多个Put操作进行合并。
⊕ [twmht/python-rocksdb: Python bindings for RocksDB](https://github.com/twmht/python-rocksdb)
    The original pyrocksdb (https://pypi.python.org/pypi/pyrocksdb/0.4) has not been updated for long time. I update pyrocksdb to support the latest rocksdb. 
⊕ [facebook/rocksdb: A library that provides an embeddable, persistent key-value store for fast storage.](https://github.com/facebook/rocksdb)
    This code is a library that forms the core building block for a fast key value server, especially suited for storing data on flash drives.
    ...
    It has multi-threaded compactions, making it specially suitable for storing multiple terabytes of data in a single database.

⊕ [Welcome to python-rocksdb’s documentation! — python-rocksdb 0.6.7 documentation](https://python-rocksdb.readthedocs.io/en/latest/)
⊕ [Basic Usage of python-rocksdb — python-rocksdb 0.6.7 documentation](https://python-rocksdb.readthedocs.io/en/latest/tutorial/index.html)

## api
⊕ [Interfaces — python-rocksdb 0.6.7 documentation](https://python-rocksdb.readthedocs.io/en/latest/api/interfaces.html#slicetransform)
⊕ [python-rocksdb-columnfamily-example/python_rocksdb_column_families_example.py at master · tkyoo/python-rocksdb-columnfamily-example](https://github.com/tkyoo/python-rocksdb-columnfamily-example/blob/master/python_rocksdb_column_families_example.py)

## start
⊕ [install problems in mac os · Issue #6 · twmht/python-rocksdb](https://github.com/twmht/python-rocksdb/issues/6)

```sh
# rocksdb: stable 5.14.3 (bottled), python-rocksdb-0.7.0.

$ brew install rocksdb
# ⊕ [npm - c++: error: unrecognized command line option '-stdlib=libc++' while installing a node package - Stack Overflow](https://stackoverflow.com/questions/38293984/c-error-unrecognized-command-line-option-stdlib-libc-while-installing-a)
# 解决issue: c++: error: unrecognized command line option '-stdlib=libc++'
$ env CC=clang CXX=clang++ pip install python-rocksdb
```
```python
>>> import rocksdb
>>> db = rocksdb.DB("out/test.db", rocksdb.Options(create_if_missing=True))
>>> db.put(b'a', b'data')
>>> print(db.get(b'a'))
b'data'
```

