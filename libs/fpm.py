import requests
import json
url = 'http://api.yunplus.io/api'
ping = 'http://api.yunplus.io/ping'
headers = {'Content-Type': 'application/json'}

class FpmLib(object):
    def __init__(self):
        pass

    def ping(self):
      r = requests.get(ping)
      return r.json()

    def call_func(self, method, params):
        
        arg_dict = {
            'appkey': '123123', 
            'method': method,
            'v': '0.0.1', 
            'timestamp':'1231', 
            'sign': '123123', 
            'param': json.dumps(params, ensure_ascii = False)
        }
        r = requests.post(url, json = arg_dict)
        rst = r.json()
        if rst['errno'] == 0:
            return rst['data']
        raise Exception(rst)

if __name__ == '__main__':
    fpm = FpmLib()
    try:
        data = fpm.call_func('common.get',{ 'table': 'api_app', 'id': 1}) 
        print json.dumps(data, ensure_ascii = False)
    except Exception as e:
        print json.dumps(e.message)