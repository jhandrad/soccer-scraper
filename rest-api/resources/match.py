from flask_restful import Resource
from models.match import MatchModel


class Matches(Resource):
    def get(self):
        return {'Jogos': [match.json() for match in MatchModel.query.all()]}

class Match(Resource):
    def get(self, id_match):
        match = MatchModel.find_match(id_match)
        if not (match is None):
            return match.json()
        return {'message': 'Not found'}, 404

