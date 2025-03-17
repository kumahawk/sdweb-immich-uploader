# Immich-pnginfo

![](misc/sss_top.png)

- This is Extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Send your creation image to [Immich](https://immich.app/) (image management software) with Generation info, tags.

## How to Install

- Go to `Extensions` tab on your web UI

- `Install from URL` with this repo URL

- Install

## How to use

- At "Immich" UI, create API key on account setting menu

- On "AUTO1111", enable this extension in "Setting" and fill server url and API key

- Create image as usual.
  
   - Output images sent to "Immich" automatically

## About Setting params

| In "Setting" tab                                                     | ![]                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Send all image to Immich"                                           | Enable this extension                                                                                                                                                                                                                                                                                                     |
| "Outside Immich server connection (url:port)"                        | (ex: https://immich.yourserver.com:2283)<br/> URL:port as Immich server address.<br/>```http://<server ip>:<port>```                                                                                                                                                                                                              |
| "Immich API key"                                                     | API key prepared in your immich account setting                                                                                                                                                                                                                                                                            |
| "Save Generation info as Annotation"                                 | Save PNGinfo style text to "memo" on Immich                                                                                                                                                                                                                                                                                |
| "Save positive prompt to Immich as tags"                             | Save each prompt word as tag on Immich                                                                                                                                                                                                                                                                                     |
| "Save negative prompt to Immich as"                                  | Save each negative prompt word as tag on Immich<br/>None  : disabled<br/>tag   : normal tag. i.e.) "bad anatomy"<br/>n:tag : tag with "n:". i.e.)"n:bad annatomy"                                                                                                                                                          |
| "Use prompt parser when save prompt to Immich as tags"               | Use prompt parser when save prompts                                                                                                                                                                                                                                                                                       |
| Additinal tag pattern                                                | Add tags about Generation info params.<br/>![](misc/sss10.png)<br />Usable word is listed,<br/>```Steps,Sampler,CFG scale,Seed,Face restoration,Size,Model hash,Model,Hypernet,Hypernet strength,Variation seed,Variation seed strength,Seed resize from,Denoising strength,Conditional mask weight,Eta,Clip skip,ENSD``` |
| FolderID or FolderName on Immich (option)                            | (option) Specify folder by ID on Immich to input images                                                                                                                                                                                                                                                                    |
| Allow to crete folder on Immich, if specified foldername dont exists.| (option) Allow create new folder with specified name, when folder with this name dont exists.                                                                                                                                                                                                                             |