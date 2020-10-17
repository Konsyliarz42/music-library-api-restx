from flask import Flask, abort
from flask_restx import Api, Resource, fields
from marshmallow import ValidationError

from models import Song, SongSchema

#================================================================
app = Flask(__name__)
api = Api(app)

song_model = api.model('Song', {    'band_name':fields.String(required=True),
                                    'album_name':fields.String(required=True),
                                    'nr':fields.Integer(required=True),
                                    'title':fields.String(required=True)})

songs = list()
#songs.append(Song("Ne Obliviscaris", "Portal Of I", 1, "Tapestry Of The Starless Abstr"))

#--------------------------------
def find_song_in_database(*, song=False, song_id=-1):
    if not songs:
        return False

    if song:
        return song in songs

    if song_id >= 0:
        try:
            return songs[song_id]
        except:
            return False

    return False

#--------------------------------
@api.route('/songs')
class SongsAll(Resource):
    @api.response(200, 'Success - Songs is loaded')
    def get(self):
        schema = SongSchema(many=True)
        result = schema.dump(songs)

        return result

    #--------------------------------
    @api.response(201, 'Created - Song is added to database')
    @api.response(400, 'Bad Request - Request is not complete or is incorrect')
    @api.response(409, 'Conflict - Song is already in database')
    @api.expect(song_model, validate=True)
    def post(self):
        try:
            result = SongSchema().load(api.payload)
        except ValidationError as error:
            return error.messages, 400

        if not find_song_in_database(song=result):
            songs.append(result)
            return {'result': 'Song is added'}, 201
        else:
            return {'result': 'Song is already in database'}, 409

#--------------------------------
@api.route('/songs/<int:song_id>')
class SongsWithID(Resource):
    @api.response(200, 'Success - Song is loaded')
    @api.response(409, 'Conflict - Song is already in database')
    def get(self, song_id):
        schema  = SongSchema()
        song    = find_song_in_database(song_id=song_id)

        if song:
            result = schema.dump(song)
            return result
        else:
            return {'result': 'Song is not find in database'}, 404

    #--------------------------------
    @api.expect(song_model, validate=True)
    @api.response(200, 'Success - Song is modified')
    @api.response(400, 'Bad Request - Request is not complete or is incorrect')
    @api.response(440, 'Not Found - Song ID is not found')
    def put(self, song_id):
        schema  = SongSchema()
        song    = find_song_in_database(song_id=song_id)

        if not song:
            return {'result': 'Song is not found in database'}, 404
        else:
            try:
                result = schema.load(api.payload)
            except ValidationError as error:
                return error.messages, 400

            songs[song_id] = result
            return {'result': 'Song is modified'}

    #--------------------------------
    @api.response(200, 'Success - Song is removed')
    @api.response(440, 'Not Found - Song ID is not found')
    def delete(self, song_id):
        if find_song_in_database(song_id=song_id):
            songs.pop(song_id)
            return {'result': 'Song is removed'}
        else:
            abort(404)

#================================================================
if __name__ == "__main__":
    app.run(debug=True)