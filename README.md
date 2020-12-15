###### tags: `github`
[![hackmd-github-sync-badge](https://hackmd.io/845fkBEuTUGqsFgdfvKykA/badge)](https://hackmd.io/845fkBEuTUGqsFgdfvKykA)

# Youtube 爬蟲下載字幕音檔

**以關鍵字搜尋 Youtube 影片，下載影片音訊及字幕**  

整合兩個套件，簡化套件的呼叫流程，加入個人化功能，在 Youtube 上尋找特定關鍵字的影片，找出具有字幕的影片，下載該影片的字幕資訊為 srt 或 xml 格式(如有)及音頻資訊為 wav 格式 (需引用 ffmpeg 套件轉換，原為 mp4 格式)

## Note

* 01/12/2020
    * 搜尋影片時只搜尋有字幕的影片，為此需要改動 youtube-search-python 的 source code
    * git clone youtube-search-python 套件，在 SearchVideos 中將條件參數改為可調整的，原固定為 "EgIQAQ%3D%3D"(影片)，現預設為 "EgQQASgB" (有字幕的影片)
    * youtube-search-python 從 pip 套件改為引用同一目錄下修改過的 source code (requirements更新)
    * 播放清單不能限制其他搜集條件，現在只有影片針對有字幕的來搜尋

## requirements
* Pytube
    * https://github.com/nficano/pytube
* youtube-search-python
    * https://github.com/alexmercerind/youtube-search-python

## Getting started
keyword search
```python
keyword = "anythink"
yts = YoutubeSearch()
v_result = yts.searchYTVideo( keyword )  # search video w/ caption only
p_result = yts.searchYTPlaylist( keyword )  # search playlist only
```

get video links of search result
```python
# the two lines get same result
urls = yts.getVideoLinks() 
urls = yts.videosResult.links  # yts.videosResult is a object of youtube-search-python
# the two lines get same result
playlists = yts.getPlaylistLinks() 
playlists = yts.playlistResult.links  # yts.playlistResult is a object of youtube-search-python
```

download caption & wav audio of a url
```python
ytdl = YoutubeDownload( savePath = "/tmp" )  # you should create the folder yourself
caption_file_path = ytdl.download_captions( url )
wav_file_path = ytdl.download_wav( url )
```

**sample code**
```python
python cw_search_download.py
```

## YoutubeSearch Object
### **class searcher.YoutubeSearch( offset: Optional[int] = 1 , mode: Optional[str] = "dict" , max_results_videos: Optional[int] = 20 , max_results_playlist: Optional[int] = 10 , language: Optional[str] = "zh-TW" , region: Optional[str] = "TW" )**  
controller of search process  

> **videosResult**

video search result, you should call this parameter after search
* **@return**   a SearchVideos Object, please read [youtube-search-python docment](https://github.com/alexmercerind/youtube-search-python)

> **playlistResult**

playlists search result, you should call this parameter after search
* **@return**   a SearchPlaylists Object, please read [youtube-search-python docment](https://github.com/alexmercerind/youtube-search-python)

> **searchYTVideo( keyword: str ) → Optional[dict,list,str]**

search video with caption and get the information by a keyword   
( but it still get video w/o caption even you chose caption in youtube search filter -.- )   
* **@parms keyword**, search keyword.
* **@return**   search result in type of self.mode, please read [youtube-search-python docment](https://github.com/alexmercerind/youtube-search-python#page_with_curl-example-result)

> **searchYTPlaylist( keyword: str ) → Optional[dict,list,str]**

search playlist and get the information by a keyword   
( playlist can't search with caption )   
* **@parms keyword**, search keyword.
* **@return**   search result in type of self.mode, please read [youtube-search-python docment](https://github.com/alexmercerind/youtube-search-python#youtube-search-python)

> **getVideoTitles() → list**

return all video's titles from search result as a list   
* **@return**   a list of titles of video search result

> **getPlaylistTitles() → list**

return all playlist's titles from search result as a list   
* **@return**   a list of titles of playlist search result

> **getVideoLinks() → list**

return all video's link from search result as a list   
* **@return**   a list of link of video search result

> **getPlaylistLinks() → list**

return all playlist's link from search result as a list   
* **@return**   a list of link of playlist search result


## YoutubeDownload Object
### **class downloader.YoutubeDownload(savePath: str)**  
controller of download process  

> **yt**

Information of a video, you should call this parameter after call getVideoInfo(url)  
recommended to call getVideoInfo to get the same result, it more safetive than call this parameter
* **@return**   a YouTube Object, please read [pytube docment ](https://python-pytube.readthedocs.io/en/latest/api.html?highlight=on_download_complete#youtube-object)

> **pl**

Information of a playlist, you should call this parameter after call getPlaylistInfo(url)  
recommended to call getPlaylistInfo to get the same result, it more safetive than call this parameter
* **@return**   a Playlist Object, please read [pytube docment ](https://python-pytube.readthedocs.io/en/latest/api.html?highlight=on_download_complete#playlist-object)

> **download_captions( url: str, fileName: Optional[str] = None , language: Optional[str] = "zh-TW" , fileType: Optional[str] = "srt" ) → str**
>     
download captions of a video url  
* **@parms url**, youtube video link url, (not a playlist link).
* **@parms fileName**, save file name without extension, optional, defaults to video title.
* **@parms language**, language of captions you want to get, optional, defaults to "zh-TW". ( however "zh-Hant" / "zh-Hant-TW" are similar to "zh-TW" )
* **@parms fileType**, save file format, should be "srt" or "xml", optional, defaults to "srt". (read pytube document get more infomation)
* **@return**   save path of caption file

> **download_wav( url: str, fileName: Optional[str] = None , keepMp4: Optional[bool] = False ) → str**

download audio as wav format of a video url  
* **@parms url**, youtube video link url (not a playlist link).
* **@parms fileName**, save file name without extension, optional, defaults to video title.
* **@parms keepMp4**, is need to keep the mp4 audio file , optional, defaults to False. (because the defaule type of audio file download from youtube is mp4)

> **download_from_playlist( playlist: str, keepMp4: Optional[bool] = False, ignoreCaption: Optional[bool] = False, language: Optional[str] = "zh-TW" , captionType: Optional[str] = "srt", dl_wav: Optional[bool] = True, dl_caption: Optional[bool] = True ) → str**

download audio & caption from a playlist, each file name default to the video title   
* **@parms playlist**, youtube playlist link url (not a video link).
* **@parms keepMp4**, is need to keep the mp4 audio file , optional, defaults to False. (because the defaule type of audio file download from youtube is mp4)
* **@parms ignoreCaption**, download videos which have caption only , optional, defaults to False.
* **@parms language**, language of captions you want to get, optional, defaults to "zh-TW". ( however "zh-Hant" / "zh-Hant-TW" are similar to "zh-TW" )
* **@parms captionType**, save caption file format, should be "srt" or "xml", optional, defaults to "srt". (read pytube document get more infomation)
* **@parms dl_wav**, is need to download audio of videos , optional, defaults to True.
* **@parms dl_caption**, is need to download caption of videos , optional, defaults to True.

> **convert_mp4_wav( infile: str, outfile: str ) → None**

convert a mp4 file to a wav file by ffmpeg package  
* **@parms infile**, input file position.
* **@parms outfile**, output file position.

> **getVideoInfo( url: str ) → pytube.YouTube**

get a video's information by a video url   
* **@parms url**, youtube link url.
* **@return**   a YouTube Object, please read [pytube docment ](https://python-pytube.readthedocs.io/en/latest/api.html?highlight=on_download_complete#youtube-object)

> **getPlaylistInfo( url: str ) → pytube.Playlist**

get a video's information by a video url   
* **@parms url**, youtube playlist url.
* **@return**   a Playlist Object, please read [pytube docment ](https://python-pytube.readthedocs.io/en/latest/api.html?highlight=on_download_complete#playlist-object)

## Todo
* change ffmpeg to python-ffmpeg
* ~~support download videos from a playlist url
(by https://github.com/nficano/pytube/issues/848)~~
* ~~search video/playlist with exist caption only (by https://github.com/alexmercerind/youtube-search-python/issues/32)~~