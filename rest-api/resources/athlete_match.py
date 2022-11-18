from flask_restful import Resource
from models.athlete_match import AthleteMatchModel


class AthletesMatches(Resource):
    def get(self):
        return {'Atletas Jogos': [athlete_match.json() for athlete_match in AthleteMatchModel.query.all()]}

class AthleteMatch(Resource):
    def get(self, id_a_m):
        athlete_match = AthleteMatchModel.find_athlete_match(id_a_m)
        if not (athlete_match is None):
            return athlete_match.json()
        return {'message': 'Not found'}, 404

