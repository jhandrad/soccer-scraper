from sql_alchemy import bd

class AthleteMatchModel(bd.Model):
    __tablename__ = 'Athletes_matches'

    id_a_m = bd.Column(bd.String,primary_key=True)
    id_fk_athlete = bd.Column(bd.String)
    id_fk_match = bd.Column(bd.Integer)
    t_r = bd.Column(bd.String)
    p_a = bd.Column(bd.String)
    num = bd.Column(bd.String)

    def __init__(self,id_a_m,id_fk_athlete,id_fk_match,
                t_r,p_a,num) -> None:
        self.id_a_m = id_a_m
        self.id_fk_athlete = id_fk_athlete
        self.id_fk_match = id_fk_match
        self.t_r = t_r
        self.p_a = p_a
        self.num = num
    
    def json(self):
        return {
            'id_a_m': self.id_a_m,
            'id_fk_athlete': self.id_fk_athlete,
            'id_fk_match': self.id_fk_match,
            't_r': self.t_r,
            'p_a': self.p_a,
            'num': self.num,
        }

    @classmethod
    def find_athlete_match(cls, id_a_m):
        athlete_match = cls.query.filter_by(id_a_m=id_a_m).first()
        if athlete_match:
            return athlete_match
        return None