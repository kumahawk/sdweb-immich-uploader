if __package__:
    from .api import Api, ImmichError
else:
    from api import Api, ImmichError
import sys

def currentuser(api: Api):
    response = api.get('/users/me')
    if not response.ok:
        raise ImmichError(response)
    json = response.json()
    return json['id']

if __name__ == '__main__':
    api = Api('https://qnapv6.arimoto.biz:32263', 'R4n9DaW6c08MgGUrgCuSN8Kuz3Dx2xQa2ccscDEE4')
    id = currentuser(api)
    print(id)