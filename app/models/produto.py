# app/models/produto.py
from app.models import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    imagem = db.Column(db.String(150))  # caminho para imagem em static/produtos
    status = db.Column(db.Boolean, default=True)    # disponível ou não
    destaque = db.Column(db.Boolean, default=False) # destaque na vitrine inicial
    # Chave estrangeira para Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome} - R${self.preco}>'