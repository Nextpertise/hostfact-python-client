from . import send_request


class Debtor(object):
    def __init__(self, url, api_key):      
        self.url = url
        self.api_key = api_key

    def add(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='debtor', action='add', **kwargs)


    def edit(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='debtor', action='edit', **kwargs)


    def debtors_list(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='debtor', action='list', **kwargs)

