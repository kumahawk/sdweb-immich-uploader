import modules.scripts as scripts
import gradio as gr
import os

from modules import shared
from modules import script_callbacks

def on_ui_settings():
    mysection = ("immich_uploader", "Immich Uploader")
    # flg: Enable/Disable
    shared.opts.add_option("enable_immich_integration", shared.OptionInfo(False, "Send all image to Immich", section=mysection))
    # flg: save generation info to annotation
    shared.opts.add_option("save_generationinfo_to_immich_as_annotation", shared.OptionInfo(False, "Save Generation info as Annotation", section=mysection))
    # flg: save positive prompt to tags
    shared.opts.add_option("save_positive_prompt_to_immich_as_tags", shared.OptionInfo(False, "Save positive prompt to Immich as tags", section=mysection))
    shared.opts.add_option("save_negative_prompt_to_immich_as", shared.OptionInfo("n:tag", "Save negative prompt as", gr.Radio, {"choices": ["None", "tag", "n:tag"]}, section=mysection))
    shared.opts.add_option("use_prompt_parser_when_save_prompt_to_immich_as_tags", shared.OptionInfo(False, "Use prompt parser when save prompt to immich as tags", section=mysection))
    # txt: Additinal tags
    shared.opts.add_option("additional_tags_to_immich", shared.OptionInfo("", "Additinal tag pattern", section=mysection))
    # txt: server_url
    shared.opts.add_option("immich_server_url_port", shared.OptionInfo("", "Outside Immich server connection (url:port)", section=mysection))
    # txt: immich API key
    shared.opts.add_option("immich_api_key", shared.OptionInfo("", "Immich API key", section=mysection))
    # specify Immich folderID
    shared.opts.add_option("save_to_immich_folderid", shared.OptionInfo("", "(option) FolderID or FolderName on Immich", component_args=shared.hide_dirs, section=mysection))
    # specify Immich folderID
    shared.opts.add_option("allow_to_create_folder_on_immich", shared.OptionInfo(False, "(option) Allow to create folder on Immich, if specified foldername dont exists.", section=mysection))

script_callbacks.on_ui_settings(on_ui_settings)
