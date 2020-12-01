import os
import sys
from youtubesearchpython import SearchVideos, SearchPlaylists

# give a keyword , search videos in Youtube
class YoutubeSearch :
    # set search key word
    # @parms offset, offset for result pages on YouTube, optional, defaults to 1.
    # @parms mode, search result return type, should be "json", "dict" or "list", optional, defaults to "dict".
    # @parms max_results_videos , maximum number of video results, optional, defaults to 20, maximum value should be 20.
    # @parms max_results_playlist , maximum number of playlist results, optional, defaults to 10, maximum value should be 20.
    # @parms language, use to get results in particular language, optional, defaults to "zh-TW".
    # @parms region, use to get results according to particular language, optional, defaults to "TW".
    def __init__( self, offset:int = 1 , mode:str = "dict" , max_results_videos:int = 20 , max_results_playlist:int = 10 , language:str = "zh-TW" , region:str = "TW" ) :
        self.offset = offset
        self.mode = mode
        self.max_results_videos = max_results_videos
        self.max_results_playlist = max_results_playlist
        self.language = language
        self.region = region
        self.videosResult = None
        self.playlistResult = None 
        return ;
    
    # search video in youtube by keyword
    # @parms keyword, search keyword
    # @return   search result in type of self.mode
    def searchYTVideo( self, keyword:str ) :
        self.videosResult = SearchVideos( keyword, offset = self.offset, mode = self.mode, max_results = self.max_results_videos, language = self.language, region = self.region )
        return self.videosResult.result() ;

    # search playlist in youtube by keyword
    # @parms keyword, search keyword
    # @return   search result in type of self.mode
    def searchYTPlaylists( self, keyword:str ) :
        self.playlistResult = SearchPlaylists( keyword, offset = self.offset, mode = self.mode, max_results = self.max_results_videos, language = self.language, region = self.region )
        return self.playlistResult.result() ;

    # return all video's titles as a list
    # @return   a list of titles of video search result
    def getVideoTitles( self ) :
        self.checkIsSearch( "videosResult" , "getVideoTitles" )
        return self.videosResult.titles ;
    
    # return all playlist's titles as a list
    # @return   a list of titles of playlist search result
    def getPlaylistTitles( self ) :
        self.checkIsSearch( "playlistResult" , "getPlaylistTitles" )
        return self.playlistResult.titles ;
    
    # return all video's link as a list
    # @return   a list of links of video search result
    def getVideoLinks( self ) :
        self.checkIsSearch( "videosResult" , "getVideoLinks" )
        return self.videosResult.links ;
    
    # return all playlist's link as a list
    # @return   a list of links of playlist search result
    def getPlaylistLinks( self ) :
        self.checkIsSearch( "playlistResult" , "getPlaylistLinks" )
        return self.videosResult.links ;
    
    # check is class already search video/playlist before
    # @parms searchType, search result object name, should be "videosResult" or "playlistResult"
    # @parms callFunction, called function name, use to print exception messages
    def checkIsSearch( self , searchType:str , callFunction:str ) :
        if searchType == "videosResult" and not self.videosResult :
            raise Exception(f"Exception : video result not exist, you should search first before you call {callFunction}!")
        elif searchType == "playlistResult" and not self.playlistResult :
            raise Exception(f"Exception : playlist result not exist, you should search first before you call {callFunction}!")
        return ;
    
if __name__ == "__main__" :  
    try :
        keyword = "微軟"
        searcher = YoutubeSearch()
        videoInfo = searcher.searchYTVideo( keyword )
        playlistInfo = searcher.searchYTPlaylists( keyword )
        print( videoInfo["search_result"][0] )
        print( playlistInfo["search_result"][0] )
        print( searcher.getVideoTitles() )
        print( searcher.getPlaylistTitles() )
        
    except Exception as e :
        print(e)
        # raise Exception("Exception Error as "+e)