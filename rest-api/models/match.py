from sql_alchemy import bd

class MatchModel(bd.Model):
    __tablename__ = 'Matches'

    id_match = bd.Column(bd.Integer,primary_key=True)
    id_championship = bd.Column(bd.Integer)
    id_h_team = bd.Column(bd.Integer)
    id_a_team = bd.Column(bd.Integer)
    stadium = bd.Column(bd.String)
    date = bd.Column(bd.String)
    round = bd.Column(bd.String)
    season = bd.Column(bd.String)

    def __init__(self,id_match,id_championship,id_h_team,
                id_a_team,stadium,date,round,season) -> None:
        self.id_match = id_match
        self.id_championship = id_championship
        self.id_h_team = id_h_team
        self.id_a_team = id_a_team
        self.stadium = stadium
        self.date = date
        self.round = round
        self.season = season

    def json(self):
        return {
            'id_match': self.id_match,
            'id_championship': self.id_championship,
            'id_h_team': self.id_h_team,
            'id_a_team': self.id_a_team,
            'stadium': self.stadium,
            'date': self.date,
            'round': self.round,
            'season': self.season
        }

    @classmethod
    def find_match(cls, id_match):
        match = cls.query.filter_by(id_match=id_match).first()
        if match:
            return match
        return None