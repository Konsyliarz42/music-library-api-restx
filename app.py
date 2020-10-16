from flask import Flask, jsonify, request
from flask_restx import Api, Resource, abort, fields

from models import Song

#================================================================
app = Flask(__name__)
api = Api(app)

songs = [
            Song('Ne Obliviscaris', 'Portal Of I', 4, 'Forget Not'),
            Song('Ne Obliviscaris', 'Citadel', 4, 'Pyrrhic'),
            Song('Ne Obliviscaris', 'Urn', 4, 'Eurie')
        ]

for i in range(len(songs)):
    songs[i] = songs[i].serialize

songs.clear()

#--------------------------------
def check_id(song_id):
    if song_id > len(songs) - 1:
        return False
    return True

#--------------------------------
@api.route('/songs')
class SongsAll(Resource):
    def get(self):
        return jsonify(songs)

    def post(self):
        try:
            data = request.get_json()
            song = Song(data['band_name'], data['album_name'], int(data['nr']), data['title']).serialize
        except ValueError:
            abort(400, message="Nr of a song in album is not a number")
        except KeyError:
            abort(409, message="Resource is not complete")
        else:
            if song in songs:
                abort(409)
            else:
                songs.append(song)
                return data, 201


#--------------------------------
@api.route('/songs/<int:song_id>')
class SongsWithID(Resource):
    def get(self, song_id):
        if check_id(song_id):
            return songs[song_id]
        else:
            abort(404)

    def put(self, song_id):
        try:
            data = request.get_json()
            song = Song(data['band_name'], data['album_name'], int(data['nr']), data['title']).serialize
        except ValueError:
            abort(400, message="Nr of a song in album is not a number")
        except KeyError:
            abort(409, message="Resource is not complete")
        else:
            if check_id(song_id):
                songs[song_id] = song
                return data
            else:
                abort(404)

    def delete(self, song_id):
        if check_id(song_id):
            songs.pop(song_id)
            return {}, 204
        else:
            abort(404)


#================================================================
if __name__ == "__main__":
    app.run(debug=True)