import requests


def send_request(url, **kwargs):  
    response = requests.post(url=url, timeout=10, verify=False, data=kwargs)
    return response.content.decode("UTF-8")