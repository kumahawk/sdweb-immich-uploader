import modules.scripts as scripts
import gradio as gr
import os, traceback
import concurrent.futures

from modules import paths, shared
from modules import script_callbacks

from scripts.parser import Parser
from scripts.tag_generator import TagGenerator
from scripts.immich.api import Api
from scripts.immich.assets import upload, update
from scripts.immich.album import Albums
from scripts.immich.tag import Tags

DEBUG = False
def dprint(str):
    if DEBUG:
        print(str)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

def uploadImage(imagefile:str, annotation:str|None, tagnames:list[str]) -> None:
    if not shared.opts.immich_server_url_port or not shared.opts.immich_api_key:
        print(f"sdweb-immich-uploader :on_image_saved: server url or key missing")
        return
    api = Api(shared.opts.immich_server_url_port, shared.opts.immich_api_key)
    dprint(f"DEBUG:on_image_saved:  uploaded image {api._url},{api._key}")
    meta = {'description': annotation} if annotation else {}
    try:
        id, _ = upload(api, imagefile, meta)
        dprint(f"DEBUG:on_image_saved:  uploaded image id {id}")
        update(api, id, meta)
        dprint(f"DEBUG:on_image_saved:  annotation {annotation}")
        if shared.opts.save_to_immich_folderid:
            albums = Albums(api)
            albums.load()
            album = albums.getbyname(shared.opts.save_to_immich_folderid)
            if album is None:
                album = albums.create(shared.opts.save_to_immich_folderid)
            album.addassets(id)
        dprint(f"DEBUG:on_image_saved:  tags {tagnames}")
        if tagnames:
            tags = Tags(api)
            tags.load()
            for tagname in tagnames:
                tag = tags.getorcreate(tagname)
                dprint(f"DEBUG:on_image_saved:  getorcreate {tagname}->{tag}->{tag._tags}->{tag._tags._api}")
                tag.tagassets(id)
        dprint(f"DEBUG:on_image_saved:  upload success")
    except Exception as e:
        print(f"DEBUG:on_image_saved:  Exception {e}")
        traceback.print_exception(e)

def on_image_saved(params:script_callbacks.ImageSaveParams) -> None:
    if not shared.opts.enable_immich_integration:
        dprint(f"DEBUG:on_image_saved:  DISABLED")
    else:
        dprint(f"DEBUG:on_image_saved:  ENABELD. enable_immich_pnginfo is true. {__package__}")
        # collect info
        fullfn = os.path.join(paths.script_path, params.filename)
        info = params.pnginfo.get('parameters', None)
        #
        pos_prompt = params.p.prompt
        neg_prompt = params.p.negative_prompt
        #
        annotation = None
        tags = []
        if shared.opts.save_generationinfo_to_immich_as_annotation:
            annotation = info
        if shared.opts.save_positive_prompt_to_immich_as_tags:
            if len(pos_prompt.split(",")) > 0:
                tags += Parser.prompt_to_tags(pos_prompt)
        if shared.opts.save_negative_prompt_to_immich_as == "tag":
            if len(neg_prompt.split(",")) > 0:
                tags += Parser.prompt_to_tags(neg_prompt)
        elif shared.opts.save_negative_prompt_to_immich_as == "n:tag":
            if len(neg_prompt.split(",")) > 0:
                tags += [ f"n:{x}" for x in Parser.prompt_to_tags(neg_prompt) ]
        if shared.opts.additional_tags_to_immich != "":
            gen = TagGenerator(p=params.p, image=params.image)
            _tags = gen.generate_from_p(shared.opts.additional_tags_to_immich)
            if _tags and len(_tags) > 0:
                tags += _tags
        executor.submit(uploadImage, fullfn, annotation, tags)

script_callbacks.on_image_saved(on_image_saved)
