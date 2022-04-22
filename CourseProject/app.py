from flask import Flask, render_template, request
from lyricsgenius import Genius
import requests

clientID = 'UGiPk4is5YU_Tnw0Uv4Hs-vqkBsCa-Eqyq53zpSfaz-e1GzEWcQ_IkGBmwp5XcFx'
clientSecret = 'PneL3rYEDMJL7dqjeZUqi55DioQFg04C6dNK-Fiy90685DQ9x5Goq1yXtgxOxMryl6b0T902SQwwulDPsQJTKg'
clientAccessToken = 'C2JI5egG5e7Mp5p1n9SA1PbS20R0_VLHxIHRSCUehuFa7llT7ETxws306TR89EzW'

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homePage():
    if request.method == "POST":
        songName = request.form["songSearch"]
        #geniusArtistSearch = f"http://api.genius.com/artists/{artistName}"
        # geniusSearchURL = f"http://api.genius.com/search?q={songName}&access_token={clientAccessToken}"
        # response = requests.get(geniusSearchURL)
        # jsonData = response.json()
        genius = Genius('C2JI5egG5e7Mp5p1n9SA1PbS20R0_VLHxIHRSCUehuFa7llT7ETxws306TR89EzW')
        artist = genius.search_artist('Radiohead', max_songs=3, sort="title")
        print(artist.songs)

    # print(jsonData)

    #print(songName)
    return render_template('hello.html')
