from genericpath import exists
from click import open_file
from flask import Flask, redirect, url_for, render_template, request
from lyricsgenius import Genius
from os import * 
import json
import requests

clientAccessToken = 'C2JI5egG5e7Mp5p1n9SA1PbS20R0_VLHxIHRSCUehuFa7llT7ETxws306TR89EzW'

app = Flask(__name__)

genius = Genius(clientAccessToken)

def songAndArtistValid(songName, artistName):
    lyrics = genius.search_song(songName, artistName)

    if path.exists('lyrics.json'):
        remove('lyrics.json')

    lyrics.save_lyrics("lyrics", ensure_ascii=True, sanitize=True)

def artistAndAlbumValid(albumName, artistName):
    album = genius.search_album(artistName, albumName)

    if path.exists('album.json'):
        remove('album.json')
            
    album.save_lyrics("album")

def artistValid(artistName):
        artist = genius.search_artists(artistName)

        if path.exists('artist.json'):
            remove('artist.json')

        with open_file('artist.json', 'w') as f:
            json.dump(artist, f, ensure_ascii=False, indent=4)

        artistFile = open_file("artist.json", "r")
        artistData = json.load(artistFile)

        artistID = artistData['sections'][0]['hits'][0]['result']['id']
        artistAlbums = genius.artist_albums(artistID)

        if path.exists('artistAlbums.json'):
            remove('artistAlbums.json')

        with open_file('artistAlbums.json', 'w') as f:
            json.dump(artistAlbums, f, ensure_ascii=False, indent=4)

@app.route("/", methods=['GET', 'POST'])
def homePage():
    if request.method == "POST":
        # get input from user, song, artist and album
        songName = request.form["userInputSong"]
        albumName = request.form["userInputAlbum"]
        artistName = request.form["userInputArtist"]

        if songName and artistName:
            songAndArtistValid(songName, artistName)
            return redirect("songLyrics")
        elif artistName and albumName: 
            artistAndAlbumValid(artistName, albumName)
            return redirect("albumList")
        elif artistName:
            artistValid(artistName)
            return redirect("artistList")

    return render_template('hello.html')

def getDataFromJSON(lyricData):
    artist = lyricData['artist']
    lyrics = lyricData['lyrics']
    songName = lyricData['title']
    songThumbImage = lyricData['song_art_image_thumbnail_url']
    songFullImage = lyricData['song_art_image_url']

    # remove extra characters at end of lyrics
    pyongCount = len(str(lyricData['pyongs_count']))
    embedCount = len('Embed')
    totalCount = pyongCount + embedCount
    lyrics = lyrics[0:len(lyrics)-totalCount]
    
    lyrics = lyrics.replace(chr(10), '<br>')

    return artist, lyrics, songName, songThumbImage, songFullImage

@app.route("/songLyrics", methods=['GET'])
def songLyrics():
    lyricsFile = open_file("lyrics.json", "r")
    lyricData = json.load(lyricsFile)

    artist, lyrics, songName, songThumbImage, songFullImage = getDataFromJSON(lyricData)

    return render_template('songLyrics.html'
                          , artist = artist
                          , lyrics = lyrics
                          , songName = songName
                          , songThumbImage = songThumbImage
                          , songFullImage = songFullImage)

def albumListParameter():
    albumFile = open_file("album.json", "r")
    albumData = json.load(albumFile)

    albumTitle = albumData['full_title']
    albumArtist = albumData['artist']['name']
    albumImage = albumData['cover_art_thumbnail_url']
    songTrackAndTitleDict = {}

    for track in albumData['tracks']:
        songTrackAndTitleDict[track['number']] = track['song']['title']
        
    return albumTitle, songTrackAndTitleDict, albumArtist, albumImage

@app.route("/albumList", methods=['GET','POST'])
def albumList():
    if request.method == "GET":
        albumTitle, albumList, albumArtist, albumImage = albumListParameter()
        return render_template('albumList.html'
                            , albumArtist = albumArtist
                            , albumList = albumList
                            , albumTitle = albumTitle
                            , albumImage = albumImage)
    else:
        songName = request.form["albumSong"]
        albumArtist = request.form["albumArtist"]
        lyrics = genius.search_song(songName, albumArtist)

        if path.exists('lyrics.json'):
            remove('lyrics.json')

        if lyrics:
            lyrics.save_lyrics("lyrics")

            return redirect("songLyrics")

        return redirect("albumList")

@app.route("/artistList", methods=['GET','POST'])
def artistList():
    if request.method == "GET":
        artistAlbumDict = {}

        artistFile = open_file("artistAlbums.json", "r")
        artistData = json.load(artistFile)

        artist = open_file("artist.json", "r")
        artistFull = json.load(artist)

        imageURL = artistFull['sections'][0]['hits'][0]['result']['image_url']
        artistName = artistFull['sections'][0]['hits'][0]['result']['name']

        wikipediaData = requests.get(f'http://localhost:9483/{artistName}?filter=band').json()
        wikiList = wikipediaData['body'].split()[:100]
        wikiList.append('...')
        wikiList = ' '.join(wikiList)

        for i, album in enumerate(artistData['albums']):
            artistAlbumDict[i] = [album['name']
                                , album['cover_art_thumbnail_url']]

        return render_template('disc.html'
                              , artistAlbums = artistAlbumDict
                              , image = imageURL
                              , artistName = artistName
                              , wikiData = wikiList)
    else:
        albumName = request.form["albumName"]
        albumArtist = request.form["albumArtist"]
        
        album = genius.search_album(albumName, albumArtist)

        if path.exists('album.json'):
            remove('album.json')
            
        album.save_lyrics("album")

        return redirect("albumList")

@app.route("/faq", methods=['GET'])
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)