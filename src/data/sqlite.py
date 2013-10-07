# -*- coding: utf-8 -*-

import os
import sqlite3

class Sqlite():
    def __init__(self, path):
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, isolation_level=None)
            else:
                raise
        except:
            pass

    def __del__(self):
        self.conn.close()

    def select(self, table, column, param=None):
        try:
            c = self.conn.cursor()
            sql = "select " + column + " from " + table
            if param:
                sql += " " + param
            c.execute(sql)
            return c.fetchall()
        except:
            return None


if __name__ == "__main__":
    # ここにメソッド書くべからず
    pass
