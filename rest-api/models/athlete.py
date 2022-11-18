from sql_alchemy import bd

class AthleteModel(bd.Model):
    __tablename__ = 'Athletes'

    id_athlete = bd.Column(bd.String,primary_key=True)
    nickname = bd.Column(bd.String)
    name = bd.Column(bd.String)
    

    def __init__(self,id_athlete,nickname,name) -> None:
        self.id_athlete = id_athlete
        self.nickname = nickname
        self.name = name
        
    def json(self):
        return {
            'id_athlete': self.id_athlete,
            'nickname': self.nickname,
            'name': self.name
        }

    @classmethod
    def find_athlete(cls, id_athlete):
        athlete = cls.query.filter_by(id_athlete=id_athlete).first()
        if athlete:
            return athlete
        return None