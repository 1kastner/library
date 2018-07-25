#!/usr/bin/python
#wrapper set

import os
import os.path
import sqlite3

class SQLiteConnectMultithreadWrapper:
    """
    Because SQLite-connections cannot be passed to another thread this workaround
    was written
    """
    def __init__(self, filename):
        if filename == ':memory:':
            if os.path.isfile('tmp_memory_database'):
                os.remove('tmp_memory_database')
            self.filename = 'tmp_memory_database'
        else:
            self.filename = filename
    def cursor(self):
        return SQLiteCursorMultithreadWrapper(self.filename) 
    def commit(self):
        return
    def __del__(self):
        #if self.filename == 'tmp_memory_database':
        #    os.remove('tmp_memory_database')
        return

class SQLiteCursorMultithreadWrapper:
    def __init__(self, filename):
        self.filename = filename
        self.result = list()
        #test file
        con = sqlite3.connect(filename)
        cur = con.cursor()
    def _connect(self):
        con = sqlite3.connect(self.filename)
        return con, con.cursor() 
    def execute(self, sqlcode, *_vars):
        con, cur = self._connect()
        if not _vars:
            cur.execute(sqlcode)
        else:
            cur.execute(sqlcode, _vars[0])
        con.commit()
        self.result = cur.fetchall()
    def fetchone(self):
        if self.result:
            res = self.result.pop(0)
            self.result = list()
            return res
        else:
            return list()
    def fetchall(self):
        if self.result:
            res = self.result[:]
            self.result = list()
            return res
        else:
            return list()
