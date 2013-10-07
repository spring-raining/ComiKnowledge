# -*- coding: utf-8 -*-

from container.list import ListContainer
import list

def merge_list(m_list, apply_color=0, apply_header=0):
    rtn = ListContainer()
    rtn.header_encoding = "UTF-8"
    rtn.header_name = m_list[apply_header].header_name
    rtn.header_id = "Co-Navigator"
    rtn.color = m_list[apply_color].color

    for i in m_list:
        if str(i) != "ListContainer":
            continue

        # i = ListContainer() # have to delete
        for j in i.circle:
            # j = CircleContainer() # have to delete
            if j in rtn.circle:
                if rtn.circle[j].color_number > i.circle[j].color_number:
                    rtn.circle[j].color_number = i.circle[j].color_number
                #TODO configで優先する色設定を変えられるようにする
                rtn.circle[j].memo += "\n" + i.circle[j].memo
            else:
                rtn.circle[j] = i.circle[j]
    return rtn



if __name__ == "__main__":
    # ここにテストを書いちゃだめ
    pass