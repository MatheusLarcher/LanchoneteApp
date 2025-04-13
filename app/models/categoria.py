# app/models/categoria.py
from app.models import db

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    ordem = db.Column(db.Integer)
    # Relação de um-para-muitos: uma categoria tem vários produtos
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nome}>'