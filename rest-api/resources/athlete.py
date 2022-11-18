from flask_restful import Resource
from models.athlete import AthleteModel


class Athletes(Resource):
    def get(self):
        return {'Atletas': [athlete.json() for athlete in AthleteModel.query.all()]}

class Athlete(Resource):
    def get(self, id_athlete):
        athlete = AthleteModel.find_athlete(id_athlete)
        if not (athlete is None):
            return athlete.json()
        return {'message': 'Not found'}, 404
