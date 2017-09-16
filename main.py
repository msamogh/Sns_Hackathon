import urllib2
from crawler import *
from downloader import *
from Tkinter import *
        
#Function to find the most appropriate video for the given search text
def initiate_Search(search):
    """
    This function extracts the Metadata of all videos on the Youtube page.
    It then finds the most relevant Metadata (and by extension, the most relevant video)
    search: the search text
    Returns: 
        a dictionary containing (key:value) pairs of metadata.
    """
    """
    ***************No error section starts****************
    """
    searchWord = search.split()
    searchStr = '+'.join(searchWord)
    base_url='https://www.youtube.com/results?search_query=' + searchStr

    try:
        soup = init(base_url)        
        metaData = getMetaData(soup, 10)
        print(metaData)

        relevant = getMostRelevant(metaData, searchWord)
        print(relevant)
        return relevant        

    except urllib2.HTTPError as e:
        print(e,'\nCould not open URL relating to',base_url)
    except urllib2.URLError as e:
        print(e,'\nCould not open URL relating to',base_url)
    except Exception as e:
        print('General exception: ', e, ' \nCould not open URL relating to',base_url)
    
    """
    ***************No error section ends******************
    """
        
#Function to download the most relevant video.
def initiate_Download(search, relevant):
    """
    This function visits https://ssyoutube.com which provides a link to download the video.
    It then downloads the video and saves it in the current directory.s
    search: the search text
    relevant: a dictionary containing (key:value) pairs of metadata.
    """
    youtube_URL = 'https://www.youtube.com'+relevant['Link']
    ssyoutube_URL = convert_youtubeURL_to_download_URL(youtube_URL)
    file_URL = retrieve_File_URL(ssyoutube_URL)
    download_video(file_URL, search+'.mp4')
        
    


