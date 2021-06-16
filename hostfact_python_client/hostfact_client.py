import os
import sys
import requests


class Method(object):
    def __init__(self, url, api_key, controller=None):      
        self.url = url
        self.api_key = api_key
        self.controller = controller

    def call(self, **kwargs):
        response = requests.post(url=self.url, timeout=10, verify=False, data={
            "api_key": self.api_key,
            "controller": self.controller,
            "action": self.name,
            **kwargs
        })
        return response.content.decode("UTF-8")

    def __getattr__(self, name):
        self.name = name
        return self.call


class HostFact(object):
    def __init__(self, url, api_key):      
        self.url = url
        self.api_key = api_key
        self.method = Method(self.url, self.api_key)


    def __getattr__(self, name):
        setattr(self.method, "controller", name)
        return self.method
        
