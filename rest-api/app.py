from flask import Flask
from flask_restful import Api

from resources.match import Matches, Match
from resources.athlete import Athletes, Athlete
from resources.championship import Championships, Championship
from resources.team import Teams, Team
from resources.athlete_match import AthletesMatches, AthleteMatch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sumulas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Matches,'/jogos')
api.add_resource(Match,'/jogos/<int:id_match>')
api.add_resource(Athletes,'/atletas')
api.add_resource(Athlete,'/atletas/<int:id_athlete>')
api.add_resource(Championships,'/campeonatos')
api.add_resource(Championship,'/campeonatos/<int:id_championship>')
api.add_resource(Teams,'/times')
api.add_resource(Team,'/times/<int:id_team>')
api.add_resource(AthletesMatches,'/atletas_jogos')
api.add_resource(AthleteMatch,'/atletas_jogos/<int:id_a_m>')

if __name__ == '__main__':
    from sql_alchemy import bd
    bd.init_app(app)
    app.run(debug=True)