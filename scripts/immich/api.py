import requests

class Api:
    _url:str
    _key:str

    def __init__(self, url:str, key:str):
        self._url = url + '/api'
        self._key = key
    
    def _headers(self, headers:dict) -> dict:
        return {"Accept": "application/json", "x-api-key": self._key} | headers

    def get(self, url:str, headers:dict = {}, **keyparams) -> requests.Response:
        return requests.get(self._url + url, headers=self._headers(headers), **keyparams)

    def post(self, url:str, headers:dict = {}, **keyparams) -> requests.Response:
        return requests.post(self._url + url, headers=self._headers(headers), **keyparams)

    def put(self, url:str, headers:dict = {}, **keyparams) -> requests.Response:
        return requests.put(self._url + url, headers=self._headers(headers), **keyparams)

    def delete(self, url:str, headers:dict = {}, **keyparams) -> requests.Response:
        return requests.delete(self._url + url, headers=self._headers(headers), **keyparams)

class ImmichError(Exception):
    _response: requests.Response
    def __init__(self, response: requests.Response):
        self._response = response       
    def __str__(self):
        try:
            json = self._response.json()
            return f"ImmichError Status={json['statusCode']} {json['error']}: {json['message']}"
        except:
            return f"ImmichError Status={self._response.status_code}: Unknown error"

if __name__ == '__main__':
    api = Api('https://qnapv6.arimoto.biz:32263', 'R4n9DaW6c08MgGUrgCuSN8Kuz3Dx2xQa2ccscDEE4')
    res = api.get('/albums')
    print(res.text)
