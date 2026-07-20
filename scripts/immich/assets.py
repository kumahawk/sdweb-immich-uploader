import os
import datetime
import hashlib
import base64

from .api import Api, ImmichError

def filedigest(path) -> bytes:
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(16*1024)
            if not data:
                break
            sha1.update(data)
        return sha1.digest()

def upload(api: Api, path:str, meta:dict):
    basename = os.path.basename(path)
    local_tz = datetime.datetime.now().astimezone().tzinfo
    btime = None
    if meta and ('btime' in meta.keys()):
        btime = datetime.datetime.fromtimestamp(meta["btime"]/1000, tz=local_tz)
    mtime = None
    if meta and ('mtime' in meta.keys()):
        mtime = datetime.datetime.fromtimestamp(meta["mtime"]/1000, tz=local_tz)
    if not(mtime and btime):
        stats = os.stat(path)
        mt = datetime.datetime.fromtimestamp(stats.st_mtime, tz=local_tz)
        if not mtime:
            mtime = mt
        if not btime:
            btime = mt
    archived = "true" if meta.get('archived') else "false"
    data = {
        "deviceAssetId": f"{basename}-{mtime.timestamp()}",
        "deviceId": "stablediffusion",
        "fileCreatedAt": btime.isoformat(),
        "fileModifiedAt": mtime.isoformat(),
        "isFavorite": "false",
        "isArchived ": archived,
    }
    digest = filedigest(path)
    files = {"assetData": open(path, "rb")}
    headers = {'x-immich-checksum': base64.b64encode(digest).decode('ascii')}
    response = api.post("/assets", headers=headers, data=data, files=files)
    response.raise_for_status()
    json = response.json()
    if "id" not in json:
        raise Exception(json.get('error', 'Unknown Error'), json.get('message', ''))
    return json["id"], json["status"]

def update(api: Api, assetid:str, meta:dict) -> None:
    if not meta:
        return
    response = api.patch(f"/assets", json=({ "ids": [ assetid ] } | meta))
    if not response.ok:
        raise ImmichError(response)