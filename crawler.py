from bs4 import BeautifulSoup
from urllib2 import urlopen, urlparse

'''
This module extracts meta data from YouTube based on the given search string using a Py module called BeautifulSoup.
'''

'''
On entering a search string in the YouTube page, there is a results page, which displays a list of relevant videos.
YouTube stores all the data about these videos using HTML format. Beautiful Soup has the capabilities to extract this HTML code and parse it.
'''

#This method initialises a Beautiful Soup object which is used to navigate through the HTML tree structure
def init(base_url):    
    """
    ***************No error section starts******************
    """
    r = urlopen(base_url).read()
    soup = BeautifulSoup(r, 'html.parser')
    return soup
    """
    ***************No error section ends******************
    """

#Returns a list of dictionaries that contain key value pairs of attribute:value
#Returns a list of dictionaries that contain key value pairs of attribute:value

'''
Each record (dictionary) of the list has the following key-value pairs

Link : string
UploadDate : string 'x months ago'
Title : string
Verified : boolean
Duration : string 'hh:mm:ss'
Channel : string
View : string

Example Dictionary:

{'Link': '/watch?v=ZynacUXphI4',
'UploadDate': '3 months ago',
'Title': 'halsey - bad at love (lyrics)',
'Verified': False,
'Duration': '3:10',
'Channel': 'hopeless',
'View': '202,583'}
'''

'''
This is a sample Tag structure in html

<div class="parent">
    <child1>
    </child1>

    <child2>
        <span>
        </span>
    </child2>
</div>

parentTag = soup.find_all("div", class_="parent")

Now parentTag contains the subtree as shown above

parentTag.contents returns a list of child Tags

The first child(child1) of parentTag can be accessed using parentTag.contents[0]
The second child(child2) of parentTag can be accessed using parentTag.contents[1]
...
The nth child of parentTag can be accessed using parentTag.content[n-1]

To access a grandchild of parentTag, we use the following

parentTag.content[1].span

'''

##

'''
<tag>
    Hello World. This is a statement
    <span>Inside the span</span>
</tag>

tag.contents returns:

Hello World. This is a statement
<span>Inside the span</span>

tag.contents[0] returns "Hello World. This is a statement"
tag.contents[1] or tag.span returns <span>Inside the span</span>

Now tag.contents[1].contents OR tag.span.contents returns "Inside the span"
'''


def getMetaData(soup, noOfRecords):
    '''
    A snippet of HTML code of the YouTube page looks like this:
    <div class="yt-lockup-content">
        <h3 class="yt-lockup-title ">
        <a aria-describedby="description-id-387243" class="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link " data-sessionlink="itct=CEQQ3DAYACITCNP33NuGpNYCFUbuaAodt4gJxyj0JFIZaGFsc2V5IGJhZCBhdCBsb3ZlIGx5cmljcw" dir="ltr" href="/watch?v=ZynacUXphI4" rel="spf-prefetch" title="halsey - bad at love (lyrics)">
            halsey - bad at love (lyrics)
            </a>
        <span class="accessible-description" id="description-id-387243">
        - Duration: 3:10.
        </span>
        </h3>
    <div class="yt-lockup-byline ">
        <a class="g-hovercard yt-uix-sessionlink spf-link " data-sessionlink="itct=CEQQ3DAYACITCNP33NuGpNYCFUbuaAodt4gJxyj0JA" data-ytid="UCEGjiQGoqJ4Plo6JkXmXnCg" href="/channel/UCEGjiQGoqJ4Plo6JkXmXnCg">
        hopeless
        </a>
        </div>
    <div class="yt-lockup-meta ">
        <ul class="yt-lockup-meta-info">
        <li>
            3 months ago
        </li>
        <li>
            202,583 views
        </li>
        </ul>
        </div>
    </div>
    '''
    
    metaData = []
    videoTags = soup.find_all("div", class_="yt-lockup-content")

    '''
    #To print all children of yt-lockup-content
    for video in videoTags:
        print(len(video.contents))
        for content in video.contents:
            print(content)
            print("\n\n")
        print("------------------------------------------------------------")
    '''
    
    #Retrieving first n records
    for i in range(min(len(videoTags), noOfRecords)):
        """
        ***************No error section starts****************
        """
        video = videoTags[i]
        d = {}

        #To remove channel tags and playlist tags
        remove = video.contents[0].contents[1]
        if(remove != None):
            if('Channel' in remove.contents[0] or 'Playlist' in remove.contents[0]):
                continue
        
        #To remove advertisement tags
        if len(video.contents) > 1:            
            s = video.contents[1].span
            if(s != None):
                if(s.has_attr('aria-label')):
                    continue
        
        #First child of yt-lockup-content division
            
        primaryData = video.contents[0].a
        durationData = video.contents[0].span
        try:
            d['Title'] = primaryData['title']
            d['Link'] = primaryData['href']
        except:
            d['Title'] = None
            d['Link'] = None
        
        """
        ***************No error section ends******************
        """

        #String manipulation for time format
        time = durationData.contents[0]
        time = time.split(' ')[-1]
        time = time.split('.')[0]
        d['Duration'] = time

        #Second child of yt-lockup-content division
        d['Channel'] = video.contents[1].a.contents[0]
        d['Verified'] = False
        if(s != None):
            if(s.has_attr('title')):
                if(s['title'] == 'Verified'):
                    pass

        #Third child of yt-lockup-content division
        metaDataTags = video.contents[2].ul
        dateLI = metaDataTags.contents[0]
        d['UploadDate'] = dateLI.contents[0]        
        try:
            viewLI = metaDataTags.contents[1]
            viewStr = viewLI.contents[0]        
            d['View'] = viewStr.split(" ")[0]
        except:
            d['View'] = "0"
        metaData.append(d)
    return metaData

#Function to check if the video has been verified.
def checkIfVerified(meta):
    return meta['Verified'] == True

#Function that converts Youtube views (a string) to an integer
#Eg: Youtube views -> 123,456,789 should become 123456789
def toNumber(string):
    number = string
    try:
        return int(number)
    except: 
        return -1

#Function that filters out the most relevant Youtube video
def getMostRelevant(metaData, searchWord):
    """
    metaData: The metadata of each of the videos in the search
    searchWord: The search text
    """
    """
    ***************No error section starts******************
    """
    #Filters only verified channels
    newMetaList = []
    for video in metaData:
        if(checkIfVerified(video)):
            newMetaList.append(video)
    if len(newMetaList) == 0:
        pass
    elif len(newMetaList) == 1:
        return newMetaList[0]
    else:
        metaData = newMetaList    

    #Filters links with closest string match to title
    
    newMetaList = []
    for video in metaData:
        missing = False
        for word in searchWord:
            if not (word in video['Title'].lower()):
                missing = True
        if missing == False:
            newMetaList.append(video)

    if len(newMetaList) == 0:
        pass
    elif len(newMetaList) == 1:
        return newMetaList[0]
    else:
        metaData = newMetaList
    
    #Chooses link with maximum number of views
        
    maxViews = toNumber(metaData[0]['View'])
    temp = metaData[0]
    for video in metaData:
        curViews = toNumber(video['View'])
        if  curViews > maxViews:
                maxViews = curViews
                temp = video
    return temp
    
    """
    ***************No error section ends******************
    """
