from flask_restful import Resource
from models.championship import ChampionshipModel


class Championships(Resource):
    def get(self):
        return {'Campeonatos': [championship.json() for championship in ChampionshipModel.query.all()]}

class Championship(Resource):
    def get(self, id_championship):
        championship = ChampionshipModel.find_championship(id_championship)
        if not (championship is None):
            return championship.json()
        return {'message': 'Not found'}, 404
