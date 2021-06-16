import os
import sys
import requests


def send_request(url, **kwargs):  
    response = requests.post(url=url, timeout=10, verify=False, data=kwargs)
    return response.content.decode("UTF-8")


class Method(object):
    def __init__(self, url, api_key, controller):      
        self.url = url
        self.api_key = api_key
        self.controller = controller

    def call(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller=self.controller, action=self.name, **kwargs)

    def __getattr__(self, name):
        self.name = name
        return self.call


class HostFact(object):
    def __init__(self, url, api_key):      
        self.url = url
        self.api_key = api_key


    def __getattr__(self, name):
        return Method(self.url, self.api_key, controller=name)
        
