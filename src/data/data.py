# -*- coding: utf-8 -*-

import sys
import os
import zipfile

from sqlite import Sqlite
from container.list import ColorContainer


def read_circle_from_dvd(txt_path, number=None, name=None):
    pass

def read_circle_from_sqlite(sqlite,):
    pass


class Ccz():
    def __init__(self, ccz_path):
        try:
            self.path = ccz_path
            self.z = zipfile.ZipFile(ccz_path)
        except:
            self.path = None

    def __del__(self):
        if self.path:
            self.z.close()

    def read_cut(self, circle_number):
        try:
            dummy = "dummy"
            while os.path.exists(dummy + ".png"):
                dummy += "_"
            dummy += ".png"
            buf = self.z.open(str(circle_number) + ".PNG", "r")
            f = open(dummy, "wb")
            f.writelines(buf)
            f.close()
            return dummy
        except:
            return

def read_cut_from_sqlite(circle_number, sqlite):
    #sqlite = Sqlite()
    try:
        dummy = "dummy"
        while os.path.exists(dummy + ".png"):
            dummy += "_"
        dummy += ".png"
        f = open(dummy, "wb")
        #print str(circle.number)
        f.write(sqlite.select("ComiketCircleImage", "cutImage", "where id='" + str(circle_number) + "'")[0][0])
        f.close()
        if not os.path.isfile(dummy):
            raise
        return dummy
    except:
        return

if __name__ == "__main__":
    pass