# app/models/pedido.py
from app.models import db
import enum
from datetime import datetime

# Definição de enums para tipo e status do pedido
class TipoPedido(enum.Enum):
    DELIVERY = 'delivery'
    RETIRADA = 'retirada'
    LOCAL = 'local'

class StatusPedido(enum.Enum):
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    EM_PREPARO = 'em_preparo'
    PRONTO = 'pronto'
    ENTREGUE = 'entregue'
    CANCELADO = 'cancelado'

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200))  # obrigatório se tipo=delivery
    # Tipo e Status usando tipo Enum do SQLAlchemy para restringir valores
    tipo = db.Column(db.Enum(TipoPedido), nullable=False, default=TipoPedido.LOCAL)
    status = db.Column(db.Enum(StatusPedido), nullable=False, default=StatusPedido.PENDENTE)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # Chave estrangeira para forma de pagamento escolhida
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey('forma_pagamento.id'))
    forma_pagamento = db.relationship('FormaPagamento')
    # Relação um-para-muitos: um pedido tem vários itens
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id} - {self.nome_cliente}>'
    
    @property
    def total(self):
        """Calcula o total do pedido somando todos os itens."""
        total = 0
        for item in self.itens:
            total += item.subtotal
        return total