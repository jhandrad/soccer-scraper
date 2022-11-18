from sql_alchemy import bd

class TeamModel(bd.Model):
    __tablename__ = 'Teams'

    id_team = bd.Column(bd.Integer,primary_key=True)
    name = bd.Column(bd.String)
    uf = bd.Column(bd.String)

    def __init__(self,id_team,name,uf) -> None:
        self.id_team = id_team
        self.name = name
        self.uf = uf
        
    def json(self):
        return {
            'id_team': self.id_team,
            'name': self.name,
            'uf': self.uf
        }

    @classmethod
    def find_team(cls, id_team):
        team = cls.query.filter_by(id_team=id_team).first()
        if team:
            return team
        return None