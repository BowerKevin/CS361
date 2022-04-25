from genericpath import exists
from click import open_file
from flask import Flask, redirect, url_for, render_template, request
from lyricsgenius import Genius
from os import * 
import json
import requests

# clientID = 'UGiPk4is5YU_Tnw0Uv4Hs-vqkBsCa-Eqyq53zpSfaz-e1GzEWcQ_IkGBmwp5XcFx'
# clientSecret = 'PneL3rYEDMJL7dqjeZUqi55DioQFg04C6dNK-Fiy90685DQ9x5Goq1yXtgxOxMryl6b0T902SQwwulDPsQJTKg'
clientAccessToken = 'C2JI5egG5e7Mp5p1n9SA1PbS20R0_VLHxIHRSCUehuFa7llT7ETxws306TR89EzW'

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homePage():
    if request.method == "POST":
        # get input from user, song, artist and album
        songName = request.form["userInputSong"]
        albumName = request.form["userInputAlbum"]
        artistName = request.form["userInputArtist"]

        # instantiate genius api with token
        genius = Genius(clientAccessToken)

        # when a user inputs song name we want to retrieve the lyrics of said song
        if songName and artistName:
            lyrics = genius.search_song(songName, artistName)

            if path.exists('lyrics.json'):
                remove('lyrics.json')

            lyrics.save_lyrics("lyrics")

            return redirect("songLyrics")
        
        elif artistName and albumName:
            album = genius.search_album(albumName, artistName)

            if path.exists('album.json'):
                remove('album.json')
            
            album.save_lyrics("album")

            return redirect("albumList")
            # print(album.tracks)
            # for track in album.tracks:
            #     print(track.number, track.song)

    return render_template('hello.html')

@app.route("/songLyrics", methods=['GET'])
def songLyrics():
    lyricsFile = open_file("lyrics.json", "r")
    lyricData = json.load(lyricsFile)
    artist = lyricData['artist']
    lyrics = lyricData['lyrics']
    songName = lyricData['title']
    
    lyrics = lyrics.replace(chr(10), '<br>')
    # print(lyrics)
    return render_template('songLyrics.html'
                          , artist=artist
                          , lyrics=lyrics
                          , songName=songName)

@app.route("/albumList", methods=['GET','POST'])
def albumList():
    albumFile = open_file("album.json", "r")
    albumData = json.load(albumFile)

    albumTitle = albumData['full_title']
    songTrackAndTitleList = []

    for track in albumData['tracks']:
        strNumAndSong = str(track['number']) + '. ' + track['song']['title']
        songTrackAndTitleList.append(strNumAndSong)

    return render_template('albumList.html'
                          , albumList=songTrackAndTitleList
                          , albumTitle = albumTitle)

