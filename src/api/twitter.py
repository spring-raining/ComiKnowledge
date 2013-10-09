# -*- coding: utf-8 -*-

import re
import requests

def get_twitter_icon_url(screen_name):
    pattern1 = re.compile('src=".+://(.+?/profile_images/.+?)"')
    pattern2 = re.compile('_(small|mini|normal|bigger|org+)')

    req = requests.get("http://twitter.com/" + screen_name)
    search = pattern1.search(req.text)
    if search:
        return "http://" + pattern2.sub("", search.group(1))
    else:
        return



if __name__ == "__main__":
    # へんじがないただのpassのようだ
    pass