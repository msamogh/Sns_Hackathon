import sqlite3
import re

def getArtists(cursor, search):
    artists =[]
    query = "SELECT artist,year,genre FROM lyrics WHERE song LIKE '%s';" %(search)
    cursor.execute(query)
    rows=cursor.fetchall()
    
    for row in rows:
        #print(row[0])        
        artists.append(row[0])
    
    return artists
    
def compareArtists(artists, search):
    for artist in artists:        
        if search == artist:            
            return artist

def searchStringLogic(cursor, search_string):
    words = search_string.split(' ')
    for i in range(len(words) - 1):
        artist = '-'.join(words[0:i+1])
        song = '-'.join(words[i+1:])
        print('Artist', artist)
        print('Song', song)
        
        artists = getArtists(cursor, song)        
        artist_result = compareArtists(artists, artist)
        if artist_result is not None:
            print(artist_result)
            return (artist_result, song)
        
    return (None, None) 
    
def getAllSongs(cursor, artist, song):
    songs = []
    query = "SELECT song, year FROM lyrics WHERE artist LIKE '%s' AND song NOT LIKE '%s';" %(artist, song)
    cursor.execute(query)
    rows=cursor.fetchall()    
    for row in rows:        
        print(row[0], row[1])
        songs.append(str(row[0]) + str(row[1]))
    return songs

def populateSongs(search):	
	try:
		conn=sqlite3.connect('ps.db')
	except sqlite3.Error as e:
		print(e)
	
	cursor = conn.cursor()

	(artist, song) = searchStringLogic(cursor, search)
	if artist is not None:
		songs = getAllSongs(cursor, artist, song)
	else:
		songs = [None]
	return songs
