from voltx import db

class Instrumentos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    temperatura = db.Column(db.String(5), nullable=False)
    umidade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Nome %r>' % self.nome


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Nome %r>' % self.nome