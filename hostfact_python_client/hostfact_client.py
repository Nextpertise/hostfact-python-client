import json

import urllib.parse, urllib.request


def http_build_query(data):
    '''http_build_query() emulates the PHP function of the same name.
    `data` can be list or dict containing nested lists or dicts of any depth.
    The output is an url encoded string that can be posted using the
    application/x-www-form-urlencoded format.
    '''
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, out = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            out += s % str(x)
            depth += 1
        return out

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs

    return urllib.parse.urlencode(r_urlencode(data))


class Method(object):
    def __init__(self, url, api_key, controller=None):      
        self.url = url
        self.api_key = api_key
        self.controller = controller

    def call(self, **kwargs):
        data={
            "api_key": self.api_key,
            "controller": self.controller,
            "action": self.name,
            **kwargs
        }
        try:
            d = http_build_query(data).encode('ascii')
            with urllib.request.urlopen(self.url, d, timeout=2) as f:
                reply = f.read()
            reply = json.loads(reply.decode('utf-8'))
        except Exception as e:
            print(f"WeFact error: {e}")
            raise

        if reply['status'] == 'error':
            print(f"WeFact error: {reply}")
            raise Exception(f"WeFact error: {reply['errors']}" if 'errors' in reply.keys() else Exception("WeFact error."))
        return reply

    def make_invoice(self, debtor_code, invoice_lines, newInvoice=False, attachment=None):
        method = Method(self.url, self.api_key, 'invoice')

        attachment_method = Method(self.url, self.api_key, 'attachment')

        active_invoices = []

        if not newInvoice:
            active_invoices = method.list(DebtorCode=debtor_code, Status=0, sort="Modified")

        if newInvoice or (not newInvoice and active_invoices['totalresults'] == 0):
            invoice_reply = method.add(DebtorCode=debtor_code, InvoiceLines=invoice_lines)
        else:
            invoice_reply = method.edit(Identifier=active_invoices['invoices'][0]['Identifier'], InvoiceLines=invoice_lines)


        if attachment:
            attachment_method.add(InvoiceCode=invoice_reply['invoice']['InvoiceCode'], Type='invoice', Filename=attachment['name'], Base64=attachment['content'])

    def __getattr__(self, name):
        if name == "make_invoice":
            return self.make_invoice
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
        
