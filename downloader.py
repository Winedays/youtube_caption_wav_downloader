import os
import subprocess
import sys
from io import BytesIO
from pytube import YouTube

# give a youtube video url , download it caption & audio as a file
class YoutubeDownload :
    # set url & files save location
    # @parms savePath, save file path, optional, defaults to run path.
    def __init__(self, savePath: str = "./") :
        if not self.checkPath( savePath ) :
            raise Exception(f"Save Path Error : save path {savePath} not exist.") 
        self.url = ""
        self.savePath = savePath
        self.yt = None
        return ;
    
    # get YouTube type object
    # @parms url, youtube link url.
    # @return   youtube type object
    def getVideoInfo( self , url ) :
        # check if this url already loaded
        if self.url != url :
            self.yt = YouTube(url)
            self.url = url
        return self.yt ;
    
    # get captions and save as srt/xml format file
    # @parms url, youtube link url.
    # @parms fileName, save file name without extension, optional, defaults to video title.
    # @parms language, language of captions you want to get, optional, defaults to "zh-TW". ( however "zh-Hant" / "zh-Hant-TW" are similar to "zh-TW" )
    # @parms fileType, save file format, should be "srt" or "xml", optional, defaults to "srt".
    # @return   save path of caption file
    def download_captions( self , url, fileName: str = None , language: str = "zh-TW" , fileType: str = "srt" ) :
        # check if this url already loaded
        self.getVideoInfo( url )
        # check parms.
        if language not in self.yt.captions :
            print( f"{sys.argv[0]}: {self.yt.watch_url} do not have {language} caption." )
            return None
        isSrt = True
        if fileType.lower() == "xml" :
            isSrt = False
        elif fileType.lower() != "srt" :
            raise Exception("Download caption type should be \"srt\" or \"xml\".")
        if not fileName :
            fileName = self.yt.title
        # download caption
        caption = self.yt.captions[language]
        originalFileName = caption.download( fileName , srt = isSrt , output_path = self.savePath )
        # re-name caption file 
        saveFile = os.path.join( self.savePath , fileName+"."+fileType )
        if originalFileName != saveFile :
            os.rename( originalFileName , saveFile )
        
        print( f"{sys.argv[0]}: {self.yt.watch_url} caption save as {saveFile}." )
        return saveFile ;
    
    # extract audio from video and save as a wav format file 
    # @parms url, youtube link url.
    # @parms fileName, save file name without extension, optional, defaults to video title.
    # @parms keepMp4, is need to keep the mp4 audio file , optional, defaults to False.
    # @return   save path of wav file
    def download_wav( self , url, fileName: str = None, keepMp4: bool = False) :
        # check if this url already loaded 
        self.getVideoInfo( url )
        # check parms.
        if not fileName :
            fileName = self.yt.title
            
        # get audio stream
        stream = self.yt.streams.get_audio_only()
        buffer = BytesIO()
        stream.stream_to_buffer( buffer )
        
        # save as a mp4 file 
        saveFile = os.path.join( self.savePath , fileName ) + "." + stream.subtype
        with open( saveFile , "wb" ) as f :
            f.write( buffer.getbuffer() )
        
        # mp4 to wav
        wavFile = os.path.join( self.savePath , fileName ) + ".wav"
        self.convert_mp4_wav( saveFile , wavFile )
        if not keepMp4 :
            os.remove( saveFile )
            print( f"{sys.argv[0]}: {self.yt.watch_url} wav audio save as {wavFile}." )
        else :
            print( f"{sys.argv[0]}: {self.yt.watch_url} wav audio save as {saveFile} & {wavFile}." )
        return wavFile ;
    
    # convert a mp4 file to wav format by ffmpeg
    # @parms infile, input file position.
    # @parms outfile, output file position.
    def convert_mp4_wav( self , infile: str , outfile: str ) :
        command = f"ffmpeg -y -i \'{infile}\' -ac 1 -ar 16000 -f wav \'{outfile}\'"
        subprocess.run(command, shell=True)
        return ;
    
    # check folder path exist
    # @parms folder, path of folder need to check
    def checkPath( self , folder ) :
        if os.path.isdir( folder ) :
            return True ;
        else :
            return False ;
    
    # check file exist
    # @parms file, path of file need to check
    def checkFile( self , file ) :
        if os.path.isfile( file ) :
            return True ;
        else :
            return False ;

    
if __name__ == "__main__" :  
    try :
        url = 'https://youtube.com/watch?v=4BOzM0lYjMw'
        downloader = YoutubeDownload( savePath = "./tmp" )
        downloader.download_captions( url , "caption" , fileType = "srt" )
        downloader.download_wav( url , "audio" )    
    except Exception as e :
        print(e)
        # raise Exception("Exception Error as "+e)