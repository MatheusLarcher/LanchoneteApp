# app/models/item_pedido.py
from app.models import db

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10,2), nullable=False)
    observacoes = db.Column(db.Text)

    # Relações para fácil acesso
    produto = db.relationship('Produto')

    def __repr__(self):
        return f'<ItemPedido {self.quantidade} x Produto {self.produto_id}>'
    
    @property
    def subtotal(self):
        """Calcula o subtotal do item (preço unitário x quantidade)"""
        return self.preco_unitario * self.quantidade