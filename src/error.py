# -*- coding: utf-8 -*-

class CoError(Exception):
    def __init__(self, reason):
        self.reason = reason

        #if reason == "HogeHoge":
        #    print "FugaFuga"

    def __str__(self):
        return self.reason

if __name__ == "__main__":
    # なにも書かないで
    pass
