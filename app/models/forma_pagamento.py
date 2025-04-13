# app/models/forma_pagamento.py
from app.models import db

class FormaPagamento(db.Model):
    __tablename__ = 'forma_pagamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<FormaPagamento {self.nome}>'