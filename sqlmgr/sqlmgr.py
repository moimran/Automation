import sqlite3
import re

class Sqlmgr(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def query(self, arg, params):
        self.cur.execute(arg, params)
        self.conn.commit()
        return self.cur

    def simplequery(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def fetchall(self):
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()