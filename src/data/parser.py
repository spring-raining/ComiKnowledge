# -*- coding: utf-8 -*-

import csv
import codecs

def parse_tab_dic(path, encoding, key_num=1):
    decoded = None
    ret = {}
    try:
        decoded = codecs.open(path, "r", encoding)
        for l in decoded:
            parsed = l.rstrip("n").split("\t")
            ret[parsed[key_num-1]] = parsed
        return ret
    except:
        pass
    finally:
        decoded.close()

def parse_tab_array(path, encoding):
    decoded = codecs.open(path, "r", encoding)
    try:
        ret = []
        for l in decoded:
            parsed = l.rstrip("\r\n").split("\t")
            ret.append(parsed)
        return ret
    finally:
        decoded.close()

def parse_checklist_array(path):
    f = open(path, "r")
    reader = csv.reader(f)
    ret = []
    encoding = "unknown"

    for l in reader:
        ret.append(l)
    for l in ret:
        if l[0] == "Header":
            if l[3] == "UTF-8":
                encoding = "utf-8"
            elif l[3] == "Shift_JIS":
                encoding = "shift-jis"
            elif l[3] == "EUC-JP":
                encoding = "euc-jp"
            elif l[3] == "ISO-2022-JP":
                encoding = "iso-2022-jp"
        break
    if encoding == "unknown":
        pass
    for l in ret:
        for i in range(len(l)):
            l[i] = l[i].decode(encoding)
    return ret


if __name__ == "__main__":
    # ここにテストを書くべからず
    pass
