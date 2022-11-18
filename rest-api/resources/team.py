from flask_restful import Resource
from models.team import TeamModel


class Teams(Resource):
    def get(self):
        return {'Times': [team.json() for team in TeamModel.query.all()]}

class Team(Resource):
    def get(self, id_team):
        team = TeamModel.find_team(id_team)
        if not (team is None):
            return team.json()
        return {'message': 'Not found'}, 404
