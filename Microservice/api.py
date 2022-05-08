from ast import keyword
from flask import Flask, render_template
import requests
from flask_restful import Resource, Api
import constants

app = Flask(__name__)
api = Api(app)

class ImageService(Resource):
    def get(self, imageKeyword):
        url = 'https://api.unsplash.com/search/photos?query={keyword}&client_id={secret}'.format(keyword=imageKeyword, secret=constants.ACCESSKEY)
        response = requests.get(url)
        data = response.json()

        imageArray = []
        for i, result in enumerate(data['results']):
            imageArray.append(result['urls']['thumb'])
            if i > 10: break
        return imageArray

api.add_resource(ImageService, '/imageService/<string:imageKeyword>')

if __name__ == '__main__':
    app.run(debug=True)