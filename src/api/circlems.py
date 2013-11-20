# -*- coding: utf-8 -*-

import requests
import json

from ComiKnowledge.settings import *

class Circlems:
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _check_status(self, dic):
        status = dic["status"]
        if status == "success":
            return True
        elif status == "access_token_denied":
            return False
        else:
            raise

    def authorization_url(self):
        url = CIRCLEMS_AUTH_URL + "OAuth2/"
        response_type = "code"
        state = "req"
        return url + "?response_type=" + response_type \
               + "&client_id=" + CIRCLEMS_CLIENT_ID \
               + "&redirect_uri=" + CIRCLEMS_REDIRECT_URL \
               + "&state=" + state \
               + "&scope=" + CIRCLEMS_SCOPE

    def get_token(self, code):
        try:
            url = CIRCLEMS_AUTH_URL + "/OAuth2/Token/"
            params = {"grant_type":"authorization_code",
                      "client_id":CIRCLEMS_CLIENT_ID,
                      "client_secret":CIRCLEMS_CLIENT_SECRET,
                      "redirect_uri":CIRCLEMS_REDIRECT_URL,
                      "code":code}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            req = requests.post(url, params=params, headers=headers)
            dic = json.loads(req.text)
            if "access_token" and "refresh_token" in dic:
                self.access_token = dic["access_token"]
                self.refresh_token = dic["refresh_token"]
                return True
            else:
                return False
        except:
            return False

    def refresh(self):
        url = CIRCLEMS_AUTH_URL + "/OAuth2/Token/"
        if self.refresh_token is None:
            raise
        try:
            params = {"grant_type":"refresh_token",
                      "client_id":CIRCLEMS_CLIENT_ID,
                      "client_secret":CIRCLEMS_CLIENT_SECRET,
                      "refresh_token":self.refresh_token}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            req = requests.post(url, params=params, headers=headers)
            dic = json.loads(req.text)
            if "access_token" and "refresh_token" in dic:
                self.access_token = dic["access_token"]
                self.refresh_token = dic["refresh_token"]
                return True
            else:
                return False
        except:
            return False

    def all(self, refreshed=False):
        url = CIRCLEMS_API_URL + "CatalogBase/All/"
        params = {"access_token":self.access_token,
                  "event_id":CIRCLEMS_EVENT_ID}
        req = requests.get(url, params=params)
        try:
            dic = json.loads(req.text)
        except ValueError:
            return None
        if not self._check_status(dic):
            if not refreshed:
                self.refresh()
                return self.all(refreshed=True)
            else:
                return dic
        else:
            return dic

    def query_circle(self, refreshed=False, circle_name=None, genre=None, floor=None, sort=1, page=None, lastupdate=None):
        url = CIRCLEMS_API_URL + "WebCatalog/QueryCircle/"
        params = {"access_token":self.access_token,
                  "event_id":CIRCLEMS_EVENT_ID,
                  "sort":sort}
        if circle_name is not None:
            params["circle_name"] = circle_name
        if genre is not None:
            params["genre"] = genre
        if floor is not None:
            params["floor"] = floor
        if page is not None:
            params["page"] = page
        if lastupdate is not None:
            params["lastupdate"] = lastupdate
        req = requests.get(url, params=params)
        try:
            dic = json.loads(req.text)
        except ValueError:
            return None
        if not self._check_status(dic):
            if not refreshed:
                self.refresh()
                return self.query_circle(refreshed=True, circle_name=circle_name, genre=genre, floor=floor, sort=sort, page=page, lastupdate=lastupdate)
            else:
                return dic
        else:
            return dic

    def get_circle(self, wcid, refreshed=False):
        url = CIRCLEMS_API_URL + "WebCatalog/GetCircle/"
        params = {"access_token":self.access_token,
                  "wcid":wcid}
        req = requests.get(url, params=params)
        try:
            dic = json.loads(req.text)
        except ValueError:
            return None
        if not self._check_status(dic):
            if not refreshed:
                self.refresh()
                return self.get_circle(wcid, refreshed=True)
            else:
                return dic
        else:
            return dic

    def favorite_circles(self, refreshed=False, circle_name=None, genre=None, floor=None, sort=1, page=None, lastupdate=None):
        url = CIRCLEMS_API_URL + "Readers/FavoriteCircles/"
        params = {"access_token":self.access_token,
                  "event_id":CIRCLEMS_EVENT_ID,
                  "sort":sort}
        if circle_name is not None:
            params["circle_name"] = circle_name
        if genre is not None:
            params["genre"] = genre
        if floor is not None:
            params["floor"] = floor
        if page is not None:
            params["page"] = page
        if lastupdate is not None:
            params["lastupdate"] = lastupdate
        print params
        req = requests.get(url, params=params)
        try:
            dic = json.loads(req.text)
        except ValueError:
            return None
        if not self._check_status(dic):
            if not refreshed:
                self.refresh()
                return self.favorite_circles(refreshed=True, circle_name=circle_name, genre=genre, floor=floor, sort=sort, page=page, lastupdate=lastupdate)
            else:
                return dic
        else:
            return dic

if __name__ == "__main__":
    # お願いしますテストは書かないでください何でもしますから！
    pass
