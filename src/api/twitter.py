# -*- coding: utf-8 -*-

import os
import re
import tempfile
import requests
import tweepy

from ComiKnowledge.settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MEDIA_ROOT
from ck.models import *
from src.utils import generate_rand_str

def save_twitter_icon(user, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    url = api.me().profile_image_url.replace("_normal", "_bigger")
    root, ext = os.path.splitext(url)
    while True:
        gen = generate_rand_str(8)
        tmp = os.path.join(MEDIA_ROOT, "thumbnails/" + gen + ext)
        if not os.path.exists(tmp):
            break
    req = requests.get(url)
    f = open(tmp, "w")
    f.write(req.content)
    f.close()
    user.thumbnail = "thumbnails/" + gen + ext
    user.save()


if __name__ == "__main__":
    # へんじがないただのpassのようだ
    pass