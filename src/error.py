# -*- coding: utf-8 -*-

class CoError(Exception):
    def __init__(self, reason):
        self.reason = reason

        #f reason == "HogeHoge":
        #    print "FugaFuga"

    def __str__(self):
        return self.reason