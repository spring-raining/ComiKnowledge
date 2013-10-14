# -*- coding: utf-8 -*-

import requests
import json

from ComiKnowledge.settings import *

class Circlems:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    def _check_status(self, dic):
        status = dic["status"]
        if status == "success":
            return True
        elif status == "access_token_denied":
            return False
        else:
            pass #TODO

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
            url = CIRCLEMS_AUTH_URL + "/OAuth2/Token"
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
        url = CIRCLEMS_AUTH_URL + "/OAuth2/Token"
        if self.refresh_token is None:
            return #TODO
        params = {"grant_type":"refresh_token",
                  "client_id":CIRCLEMS_CLIENT_ID,
                  "client_secret":CIRCLEMS_CLIENT_SECRET,
                  "redirect_uri":CIRCLEMS_REDIRECT_URL,
                  "access_token":self.access_token,
                  "refresh_token":self.refresh_token}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        req = requests.post(url, params=params, headers=headers)
        return req.text

    def all(self):
        url = CIRCLEMS_API_URL + "CatalogBase/All/"
        params = {"access_token":self.access_token,
                  "event_id":CIRCLEMS_EVENT_ID}
        req = requests.get(url, params=params)
        dic = json.loads(req.text)
        if not self._check_status(dic):
            return self.refresh()
        else:
            return dic

    def query_circle(self, circle_name=None, genre=None, floor=None, sort=1, page=None, lastupdate=None):
        url = CIRCLEMS_API_URL + "WebCatalog/QueryCircle"
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
        return req.text

    def get_circle(self, wcid):
        url = CIRCLEMS_API_URL + "WebCatalog/GetCircle/"
        params = {"access_token":self.access_token,
                  "wcid":wcid}
        req = requests.get(url, params=params)
        return req.text

    def favorite_circles(self, circle_name=None, genre=None, floor=None, sort=1, page=None, lastupdate=None):
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
        req = requests.get(url, params=params)
        return req.text


if __name__ == "__main__":
    # お願いしますテストは書かないでください何でもしますから！
    pass