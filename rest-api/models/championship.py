from sql_alchemy import bd

class ChampionshipModel(bd.Model):
    __tablename__ = 'Championship'

    id_championship = bd.Column(bd.Integer,primary_key=True)
    name = bd.Column(bd.String)
    
    def __init__(self,id_championship,name) -> None:
        self.id_championship = id_championship
        self.name = name
        
    def json(self):
        return {
            'id_championship': self.id_championship,
            'name': self.name
        }

    @classmethod
    def find_championship(cls, id_championship):
        championship = cls.query.filter_by(id_championship=id_championship).first()
        if championship:
            return championship
        return None