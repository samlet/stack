import os
import sys
import shutil
import gc
import rocksdb
from itertools import takewhile
import struct
import tempfile
from rocksdb.merge_operators import UintAddOperator, StringAppendOperator

def int_to_bytes(ob):
    return str(ob).encode('ascii')

def get_columns(db_loc, name):
    cols = rocksdb.list_column_families(
        os.path.join(db_loc, name),
        rocksdb.Options(),
    )
    return cols

class DataSpace(object):
    def __init__(self, name, fields):
        """
        init a data space
        :param name:
        :param fields: [b'A', b'B']
        """
        self.db_loc = './db'
        opts = rocksdb.Options(create_if_missing=True)
        # self.columns = {}
        if os.path.exists(os.path.join(self.db_loc, name)):
            column_families = {}
            for fld in fields:
                column_families[fld] = rocksdb.ColumnFamilyOptions()
            self.db = rocksdb.DB(os.path.join(self.db_loc, name), opts, column_families=column_families)
            # self.columns = column_families
        else:
            self.db = rocksdb.DB(os.path.join(self.db_loc, name), opts)
            for fld in fields:
                # fld format: b'A'
                # self.columns[fld]=(self.db.create_column_family(fld, rocksdb.ColumnFamilyOptions()))
                self.db.create_column_family(fld, rocksdb.ColumnFamilyOptions())

    def cleanup_db(self):
        del self.db
        gc.collect()
        if os.path.exists(self.db_loc):
            shutil.rmtree(self.db_loc)

    def column_names(self):
        families = self.db.column_families
        names = [handle.name for handle in families]
        return names

    def col(self, column_name):
        return self.db.get_column_family(column_name)

    def put(self, key, column_name, val):
        cf=self.col(column_name)
        self.db.put((cf, key), val)

    def put_proto(self, key, column_name, val):
        self.put(key, column_name, val.SerializeToString())

    def delete(self, key, column_name):
        cf = self.col(column_name)
        self.db.delete((cf, key))

    def get(self, key, column_name):
        cf = self.col(column_name)
        return self.db.get((cf, key))

    def get_proto(self, key, column_name, proto):
        val=self.get(key, column_name)
        proto.ParseFromString(val)
        return proto

    def exists(self, key, column_name, fetch=True):
        """
        Check key/col exists
        :param key:
        :param column_name:
        :param fetch:
        :return: (False, None) or (True, None) or (True, b'1')
        """
        cf = self.col(column_name)
        return self.db.key_may_exist((cf, key), fetch=fetch)

    def all_column_values(self, column_name):
        cf = self.col(column_name)
        it = self.db.iteritems(cf)
        it.seek_to_last()
        return list(it)

sys_db=DataSpace('sys.db', [b'property', b'value'])

