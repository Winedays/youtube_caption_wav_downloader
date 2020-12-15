import os
import sys
from downloader import YoutubeDownload
from searcher import YoutubeSearch

# give a keyword , search videos in Youtube , download caption & wav
class Youtube :
    # initial yt. searcher
    # @parms savePath, save file path, optional, defaults to run path.
    # @parms max_results_videos , maximum number of video results, optional, defaults to 20, maximum value should be 20.
    # @parms max_results_playlist , maximum number of playlist results, optional, defaults to 10, maximum value should be 20.
    # @parms language, use to get results in particular language, optional, defaults to "zh-TW".
    # @parms region, use to get results according to particular language, optional, defaults to "TW".
    def __init__( self , savePath = "./" , max_results_videos = 20 , max_results_playlist = 10 , language = "zh-TW" , region = "TW" ) :
        offset = 1
        mode = "dict"
        self.language = language
        self.searcher = YoutubeSearch( offset = offset, mode = mode, max_results_videos = max_results_videos, max_results_playlist = max_results_playlist, language = language, region = region )
        self.downloader = YoutubeDownload( savePath = savePath )
        return ;

    # search by keyword, download videos of search result
    # @parms keyword, search keyword
    # @parms savePath, save file path, optional, defaults to run path.
    def downloadRelatedVideos( self, keyword:str, savePath:str = "./" ) :
        # search
        self.searcher.searchYTVideo( keyword )
        self.searcher.searchYTPlaylist( keyword )  
        # download videos
        count = 0 ;  #  count downloaded video
        linkList = self.searcher.getVideoLinks()
        # download each video's audio & caption
        for link in linkList :
            if self.downloader.download_captions( link , language = self.language , fileType = "srt" )  :
                self.downloader.download_wav( link , keepMp4 = False )
                count += 1 
        print( f"{sys.argv[0]}: download {str(count)} videos's wav & caption of keyword \"{keyword}\"." )
        # download each playlist video's audio & caption
        playlistList = self.searcher.getPlaylistLinks()
        for playlist in playlistList :
            self.downloader.download_from_playlist( playlist , keepMp4 = False , language = self.language , captionType = "srt"  )
        return ;
    
if __name__ == "__main__" :  
    try :
        keyword = "TED 台灣"
        savePath = "./tmp"
        yt = Youtube( savePath = savePath , max_results_videos = 5 , max_results_playlist = 1 )
        yt.downloadRelatedVideos( keyword )
        
    except Exception as e :
        print(e)
        # raise Exception("Exception Error as "+e)