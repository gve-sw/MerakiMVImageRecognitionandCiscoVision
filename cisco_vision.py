import requests
from env_var import base_url

def default():
    url = "{0}/1".format(base_url)
    response = requests.request("GET", url, headers={}, data={})
    print(response.status_code)
    
def child():
    url = "{0}/2".format(base_url)
    response = requests.request("GET", url, headers={}, data={})
    print(response.status_code)
    
def male():
    url = "{0}/3".format(base_url)
    response = requests.request("GET", url, headers={}, data={})
    print(response.status_code)
    
 def female():
    url = "{0}/4".format(base_url)
    response = requests.request("GET", url, headers={}, data={})
    print(response.status_code)
    
