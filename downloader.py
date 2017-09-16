from bs4 import BeautifulSoup
import dryscrape
import requests
import time

#Function to change https://www.youtube.com/XXX to https://www.ssyoutube.com/XXX
def convert_youtubeURL_to_download_URL(youtube_URL):
	"""
	https://www.ssyoutube.com/XXX contains a link which allows music videos to be downloaded.
	youtube_URL: the URL of the music video to be downloaded
	"""
	index = youtube_URL.find('youtube')
	file_retrieve_URL = youtube_URL[0:index] + 'ss' + youtube_URL[index:]
	redirect_response = requests.get(file_retrieve_URL)
	print(redirect_response.url)
	return redirect_response.url

#Function which looks for the exact download location of the music video.
#This is distinct from the https://www.ssyoutube.com/XXX URL.
#Go ahead, open up the browser console and look for the URL that I'm talking about.
def retrieve_File_URL(ss_downloaded_URL):
	"""
	ss_downloaded_URL: contains the URL of the music video. (https://www.ssyoutube.com/XXX)
	***************No error section starts****************
	"""
	
	sess = dryscrape.Session()
	sess.visit(ss_downloaded_URL)
	time.sleep(10)
	response = sess.body()
	response = response.encode('ascii', 'ignore')	
	soup = BeautifulSoup(response.decode('ascii', 'ignore'), 'html.parser')	
	div = soup.find('div', {'class':'def-btn-box'})	
	print('*************************')	
	anchor = div.find('a')
	print('*************************')
	print(anchor['href'])
	return anchor['href']
	
	"""
	***************No error section ends******************
	"""

#Function to download the music video.	
def download_video(url, filename):
	"""
	url: The exact download location of the music video.
	filename: The downloaded video is stored as filename.mp4
	***************No error section starts****************
	"""
	headers = {
		'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		'accept-encoding': "gzip, deflate, br"    
		}

	"""
	***************No error section ends******************
	"""
	
	response = requests.get(url, headers=headers)
	print(response)
	file = open(filename, 'wb')
	file.write(response.content)
	file.close()
