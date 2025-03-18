from .api import Api, ImmichError

def currentuser(api: Api):
    response = api.get('/users/me')
    if not response.ok:
        raise ImmichError(response)
    json = response.json()
    return json['id']