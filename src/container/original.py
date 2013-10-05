# -*- coding: utf-8 -*-

import json
import uuid
from PySide import QtCore

from container.list import CircleContainer


class OriginalCircleContainer(CircleContainer):
    def __init__(self):
        CircleContainer.__init__(self)
        self.want = None #買いたい人を表すコンテナID
        self.buy = None #これを買う人を表すコンテナID

class OriginalMemberContainer:
    def __init__(self):
        self.id = str(uuid.uuid4()) # 一意のコンテナID
        self.same_member = [] # 同じメンバーの過去のIDの配列
        self.comiket_number = None # 参加したコミケの回数番号
        self.want = [] # 買いたい物のIDの配列
        self.buy = [] # 買う物のIDの配列
        self.attend = {} # 参加日時 TODO:参加日時のデータ形式の決定
        self.name = None # メンバーの名前
        self.name_yomigana = None # メンバーのふりがな
        self.handle = None # メンバーのハンドルネーム
        self.address = None # メンバーのアドレス
        self.tel = None # メンバーの電話番号
        self.twitter_id = None # メンバーのTwitter ID
        self.skype_id = None # メンバーのSkype ID

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def import_json(self, text):
        try:
            dic = json.loads(text)
            for k, v in dic.items():
                if hasattr(self, k):
                    self[k] = v
        except:
            pass


    def load_setting(self, settings):
        #settings = QtCore.QSettings()
        settings.beginGroup("profile")
        for k in settings.allKeys():
            if hasattr(self, k):
                self[k] = settings.value(k)
        settings.endGroup()

    def save_setting(self, settings):
        #settings = QtCore.QSettings()
        settings.beginGroup("profile")
        for k, v in self.__dict__.items():
            if v:
                settings.setValue(k, v)
            else:
                settings.remove(k)
        settings.endGroup()

if __name__ == "__main__":
    test_member = OriginalMemberContainer()
    #print test_member.id
    test_member.import_json("AHO")
