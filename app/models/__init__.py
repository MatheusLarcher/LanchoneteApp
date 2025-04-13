# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para facilitar o acesso
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.forma_pagamento import FormaPagamento
from app.models.pedido import Pedido, TipoPedido, StatusPedido
from app.models.item_pedido import ItemPedido