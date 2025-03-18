from __future__ import annotations
from typing import Any
import json
from .api import Api, ImmichError

class Tag:
    _json: dict[str, Any]
    _parent: Tag|None
    _tags: Tags

    def __init__(self, tags: Tags, json: dict[str, Any], parent:Tag|None = None):
        self._json = json
        self._tags = tags
        self._parent = parent

    def __getattr__(self, name: str) -> Any:
        value = self._json.get(name)
        if value is not None:
            setattr(self, name, value)
        return value

    def tagassets(self, *ids:str) -> None:
        data = json.dumps({ "ids":  ids })
        header = { "content-type": "application/json" }
        response = self._tags._api.put(f'/tags/{self.id}/assets', headers=header, data=data)
        if not response.ok:
            raise ImmichError(response)

class Tags:
    _tags: dict[str, Tag]
    _api: Api

    def __init__(self, api: Api):
        self._api = api
        self._tags = {}
    
    def load(self) -> None:
        response = self._api.get('/tags')
        if not response.ok:
            raise ImmichError(response)
        json = response.json()
        for taginfo in json:
            tag = Tag(self, taginfo)
            self._tags[tag.id] = tag
        for tag in self._tags.values():
            if tag.parentid and tag._parent is None:
                tag._parent = self.getbyid(tag.parentid)
    
    def getbyid(self, id: str) -> Tag|None:
        return self._tags.get(id)
    
    def getbyname(self, name: str, parent:Tag|None = None) -> Tag|None:
        parentid = parent.id if parent else None
        for tag in self._tags.values():
            if tag.name == name and tag.parentid == parentid :
                return tag
        return None
    
    def getbynames(self, names: list[str]) -> Tag|None:
        parentid = None
        tag = None
        for name in names:
            tag = self.getbyname(name, parentid)
            if tag is None:
                return None
            parentid = tag.id
        return tag

    def getorcreate(self, name: str, parent:Tag|None = None) -> Tag:
        tag = self.getbyname(name, parent)
        if tag is None:
            tag = self.create(name, parent)
        return tag
    
    def createbynames(self, name0:str, *names: str) -> Tag:
        tag = self.getorcreate(name0)
        for name in names:
            tag = self.getorcreate(name, tag)
        return tag
    
    def create(self, name: str, parent:Tag|None = None) -> Tag:
        data = { "name": name, "parentId": parent.id } if parent else { "name": name }
        response = self._api.post('/tags', data=data)
        if not response.ok:
            raise ImmichError(response)
        json = response.json()
        tag = Tag(self, json, parent)
        self._tags[json['id']] = tag
        return tag