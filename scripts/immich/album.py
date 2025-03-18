from __future__ import annotations
from typing import Any
from .api import Api, ImmichError
from .user import currentuser

class Album:
    _json: dict[str, Any]
    _albums: Albums

    def __init__(self, albums: Albums, json: dict[str, Any]):
        self._json = json
        self._albums = albums

    def __getattr__(self, name: str) -> Any:
        value = self._json.get(name)
        if value is not None:
            setattr(self, name, value)
        return value

    def addassets(self, *ids:str) -> None:
        data = { "ids":  ids }
        response = self._albums._api.put(f'/albums/{self.id}/assets', json=data)
        if not response.ok:
            raise ImmichError(response)
    
class Albums:
    _albums: dict[str, Album]
    _api: Api

    def __init__(self, api: Api):
        self._api = api
        self._albums = {}
    
    def load(self) -> None:
        response = self._api.get('/albums')
        if not response.ok:
            raise ImmichError(response)
        json = response.json()
        for albuminfo in json:
            album = Album(self, albuminfo)
            self._albums[album.id] = album
    
    def getbyid(self, id: str) -> Album|None:
        return self._albums.get(id)
    
    def getbyname(self, name: str) -> Album|None:
        for album in self._albums.values():
            if album.albumName == name:
                return album
        return None
    
    def create(self, name: str) -> Album:
        data = {
            "albumName": name,
            "albumUsers": [
                {
                "role": "editor",
                "userId": currentuser(self._api)
                }
            ]
        }
        response = self._api.post('/albums', json=data)
        if not response.ok:
            raise ImmichError(response)
        json = response.json()
        album = Album(self, json)
        self._albums[json['id']] = album
        return album
