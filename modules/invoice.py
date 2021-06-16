from . import send_request


class Invoice(object):
    def __init__(self, url, api_key):      
        self.url = url
        self.api_key = api_key

    def add(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='invoice', action='add', **kwargs)


    def edit(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='invoice', action='edit', **kwargs)


    def invoices_list(self, **kwargs):
        return send_request(url=self.url, api_key=self.api_key, controller='invoice', action='list', **kwargs)

