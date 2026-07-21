import os, traceback
import concurrent.futures

from modules import paths, shared
from modules import prompt_parser
from modules import script_callbacks

from scripts.tag_generator import TagGenerator
from scripts.immich.api import Api
from scripts.immich.assets import upload, update
from scripts.immich.album import Albums
from scripts.immich.tag import Tags

DEBUG = False
def dprint(str):
    if DEBUG:
        print(str)

def pickuptags(description: str) -> list[str]:
    tags = []
    if description:
        if description.find('from behind') >= 0:
            if description.find('ass') >= 0:
                tags.append('お尻')
        if description.find('school swimsuit') >= 0:
            tags.append('スク水')
        elif description.find('swimsuit') >= 0:
            tags.append('水着')
        elif description.find('swimware') >= 0:
            tags.append('水着')
        elif description.find('bikini') >= 0:
            tags.append('水着')
        if description.find('wedding') >= 0:
            tags.append('ウェディング')
        elif description.find('bridal') >= 0:
            tags.append('ウェディング')
        if description.find('1boy') >= 0:
            if description.find('sissy') >= 0:
                tags.append('おとこの娘')
            elif description.find('girlish') >= 0:
                tags.append('おとこの娘')
        if description.find('business') >= 0:
            tags.append('スーツ')
        elif description.find('office') >= 0:
            tags.append('スーツ')
        if description.find('school uniform') >= 0:
            tags.append('制服')
        if description.find('gym uniform') >= 0:
            tags.append('ブルマ')
        if description.find('pussy juice') >= 0:
            tags.append('汁')
        if description.find('milf') >= 0:
            tags.append('熟女')
        elif description.find('mature female') >= 0:
            tags.append('熟女')
        elif description.find('mature woman') >= 0:
            tags.append('熟女')
        if description.find('magical girl') >= 0:
            tags.append('魔法少女')
        if description.find('maid') >= 0:
            tags.append('メイド')
        if description.find('nurse') >= 0:
            tags.append('ナース')
        if description.find('lingerie') >= 0:
            tags.append('ランジェリー')
        elif description.find('babydoll') >= 0:
            tags.append('ランジェリー')
        elif description.find('slip') >= 0:
            tags.append('ランジェリー')
        if description.find('large breasts') >= 0:
            tags.append('大胸')
        elif description.find('huge breasts') >= 0:
            tags.append('超胸')
        elif description.find('medium breasts') >= 0:
            tags.append('中胸')
        elif description.find('small breasts') >= 0:
            tags.append('小胸') 
        if description.find('restrained') >= 0:
            tags.append('拘束')
    return tags

def uploadImage(imagefile:str, annotation:str|None, tagnames:list[str]) -> None:
    if not shared.opts.immich_server_url_port or not shared.opts.immich_api_key:
        print(f"sdweb-immich-uploader: on_image_saved: server url or key missing")
        return
    api = Api(shared.opts.immich_server_url_port, shared.opts.immich_api_key)
    dprint(f"DEBUG:on_image_saved:  uploaded image {api._url},{api._key}")
    try:
        meta = {}
        if annotation:
            meta['description'] = annotation
        if shared.opts.immich_archive_after_upload:
            meta['visibility'] = 'archive'
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

def prompt_to_tags(p):
    use_prompt_parser = shared.opts.use_prompt_parser_when_save_prompt_to_immich_as_tags

    if use_prompt_parser:
        return [ x[0].strip() for x in prompt_parser.parse_prompt_attention(p) ]
    else:
        return [ x.strip() for x in p.split(",") if x.strip() != "" ]

executor = None

def on_image_saved(params:script_callbacks.ImageSaveParams) -> None:
    global executor
    if not shared.opts.enable_immich_integration:
        dprint(f"DEBUG:on_image_saved:  DISABLED")
    else:
        dprint(f"DEBUG:on_image_saved:  ENABELD. enable_immich_pnginfo is true.")
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
        if params.filename.find('grid-') >= 0:
            tags.append('グリッド')
        else:
            tags += pickuptags(pos_prompt)
        info = params.pnginfo.get('parameters', None)
        if shared.opts.save_positive_prompt_to_immich_as_tags:
            if len(pos_prompt.split(",")) > 0:
                tags += prompt_to_tags(pos_prompt)
        if shared.opts.save_negative_prompt_to_immich_as == "tag":
            if len(neg_prompt.split(",")) > 0:
                tags += prompt_to_tags(neg_prompt)
        elif shared.opts.save_negative_prompt_to_immich_as == "n:tag":
            if len(neg_prompt.split(",")) > 0:
                tags += [ f"n:{x}" for x in prompt_to_tags(neg_prompt) ]
        if shared.opts.additional_tags_to_immich != "":
            gen = TagGenerator(p=params.p, image=params.image)
            _tags = gen.generate_from_p(shared.opts.additional_tags_to_immich)
            if _tags and len(_tags) > 0:
                tags += _tags
        num_threads = shared.opts.immich_upload_threads_number
        if num_threads <= 0:
            uploadImage(fullfn, annotation, tags)
        else:
            if executor is None:
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
            executor.submit(uploadImage, fullfn, annotation, tags)

script_callbacks.on_image_saved(on_image_saved)
