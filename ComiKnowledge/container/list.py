# -*- coding: utf-8 -*-

class ListContainer:
    def __init__(self):
        self.circle = {}
        self.unknown = {}
        self.color = {}
        self.header_name = None
        self.header_encoding = None
        self.header_id = None
        self.last_select_page = None
        self.last_select_circle = None
        self.mac_print_info = None

    def __str__(self):
        return "ListContainer"




class CircleContainer:
    def __init__(self):
        self.number = None
        self.color_number = None
        self.page_number = None
        self.cut_index = None
        self.week = None
        self.area = None
        self.block = None
        self.space_number = None
        self.genre = None
        self.name = None
        self.name_yomigana = None
        self.author = None
        self.issue = None
        self.url = None
        self.mail = None
        self.appendix = None
        self.memo = None
        self.map_x = None
        self.map_y = None
        self.layout = None
        self.space_position = None
        self.update = None
        self.circlems_url = None
        self.rss = None
        self.rss_data = None

    def __str__(self):
        return "CircleContainer"

    def space_long(self):
        if self.area is None or self.block is None or self.space_number is None or self.space_position is None:
            space = ""
        else:
            if self.area == "" or self.block == "" or str(self.space_number) == "":
                space = ""
            else:
                space = self.area + self.block + "-" + str(self.space_number)
                if self.space_position == 0:
                    space += "a"
                elif self.space_position == 1:
                    space += "b"
                else:
                    space = ""
        return space



class UnKnownContainer:
    def __init__(self):
        self.name = None
        self.name_yomigana = None
        self.author = None
        self.memo = None
        self.color = None
        self.issue = None
        self.url = None
        self.mail = None
        self.appendix = None
        self.update = None
        self.circlems_url = None
        self.rss = None

    def __str__(self):
        return "UnKnownContainer"




class ColorContainer:
    def __init__(self):
        self.color_number = None
        self.check_color = None
        self.print_color = None
        self.description = None

    def __str__(self):
        return "ColorContainer"

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def load_setting(self, settings, number):
        #settings = QtCore.QSettings()
        settings.beginGroup("color" + str(number))
        for k in settings.allKeys():
            if hasattr(self, k):
                self[k] = settings.value(k)
        settings.endGroup()

    def save_setting(self, settings, number):
        #settings = QtCore.QSettings()
        settings.beginGroup("color" + str(number))
        for k, v in self.__dict__.items():
            if v:
                settings.setValue(k, v)
            else:
                settings.remove(k)
        settings.endGroup()