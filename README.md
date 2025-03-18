# Immich-uploader

![](misc/sss_top.png)

- This is Extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Send your creation image to [Immich](https://immich.app/) (photo management server) with Generation info, tags.

## Disclaimer

This extension is inspired by [sdweb-eagle-pnginfo](https://github.com/kumahawk/sdweb-eagle-pnginfo) and
plenty of code was from theirs ##special thanks

## How to Install

- Go to `Extensions` tab on your web UI

- `Install from URL` with this repo URL

- Install and restart web UI

## How to use

- On "Immich" UI, create API key in "account setting"

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
| Number of background upload threads(0:disable background upload).    | Number of threads to upload images to Immich server in background. If this is 0, disable background upload.                                                                                                                                                                                                                              |
| Archive images after upload                                          | Archive images after upload is done immediately.                                                                                                                                                                                                                         |
