import os
import sys
import requests


from collections import namedtuple


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)


from modules.invoice import Invoice
from modules.debtor import Debtor


class HostFact(object):
    def __init__(self, url, api_key):      
        self.url = url
        self.api_key = api_key

        self.invoice = Invoice(self.url, self.api_key)
        self.debtor = Debtor(self.url, self.api_key)

    def call(self, controller, action, **kwargs):
        response = requests.post(url=self.url, timeout=10, verify=False, data={
            "api_key": self.api_key,
            "controller": controller,
            "action": action,
            **kwargs
        })
        return response.content.decode("UTF-8")

    # def call(self, controller, action, params=None):
    #     args = {
    #         'api_key': self.api_key,
    #         'controller': controller,
    #         'action': action
    #     }
        
