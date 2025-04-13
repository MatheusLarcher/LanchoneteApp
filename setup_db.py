# setup_db.py
from app import create_app
from app.models import db
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.forma_pagamento import FormaPagamento
from app.models.pedido import Pedido, TipoPedido, StatusPedido
from app.models.item_pedido import ItemPedido
from datetime import datetime

app = create_app()

def setup_database():
    with app.app_context():
        print("Criando tabelas...")
        db.drop_all()
        db.create_all()
        
        print("Populando dados iniciais...")
        # Categorias
        cat1 = Categoria(nome="Bebidas", descricao="Bebidas geladas e quentes", ordem=1)
        cat2 = Categoria(nome="Lanches", descricao="Sanduíches e hamburgers", ordem=2)
        cat3 = Categoria(nome="Porções", descricao="Porções para compartilhar", ordem=3)
        cat4 = Categoria(nome="Sobremesas", descricao="Doces e sobremesas", ordem=4)
        
        db.session.add_all([cat1, cat2, cat3, cat4])
        db.session.flush()
        
        # Produtos
        prod1 = Produto(nome="Refrigerante Lata", descricao="350ml - Coca-cola", 
                        preco=5.00, imagem="refrigerante.jpg", categoria_id=cat1.id, 
                        status=True, destaque=True)
        
        prod2 = Produto(nome="Suco Natural", descricao="Copo 300ml - Laranja, Limão, Abacaxi", 
                        preco=7.50, imagem="suco.jpg", categoria_id=cat1.id, 
                        status=True, destaque=False)
        
        prod3 = Produto(nome="X-Burger", descricao="Hambúrguer clássico com queijo, alface, tomate e molho especial", 
                        preco=15.00, imagem="xburger.jpg", categoria_id=cat2.id, 
                        status=True, destaque=True)
        
        prod4 = Produto(nome="X-Salada", descricao="Hambúrguer com queijo, alface, tomate, cebola, milho e maionese", 
                        preco=17.00, imagem="xsalada.jpg", categoria_id=cat2.id, 
                        status=True, destaque=False)
        
        prod5 = Produto(nome="Batata Frita", descricao="Porção de batatas fritas crocantes (300g)", 
                        preco=12.00, imagem="batata.jpg", categoria_id=cat3.id, 
                        status=True, destaque=True)
        
        prod6 = Produto(nome="Onion Rings", descricao="Anéis de cebola empanados (10 unidades)", 
                        preco=14.00, imagem="onion.jpg", categoria_id=cat3.id, 
                        status=True, destaque=False)
        
        prod7 = Produto(nome="Sorvete", descricao="Casquinha de sorvete nos sabores chocolate, morango ou creme", 
                        preco=8.00, imagem="sorvete.jpg", categoria_id=cat4.id, 
                        status=True, destaque=False)
        
        prod8 = Produto(nome="Milkshake", descricao="Milkshake cremoso nos sabores chocolate, morango ou baunilha (400ml)", 
                        preco=12.00, imagem="milkshake.jpg", categoria_id=cat4.id, 
                        status=True, destaque=True)
        
        db.session.add_all([prod1, prod2, prod3, prod4, prod5, prod6, prod7, prod8])
        
        # Formas de Pagamento
        fp1 = FormaPagamento(nome="Dinheiro")
        fp2 = FormaPagamento(nome="Cartão de Crédito")
        fp3 = FormaPagamento(nome="Cartão de Débito")
        fp4 = FormaPagamento(nome="Pix")
        
        db.session.add_all([fp1, fp2, fp3, fp4])
        
        # Commit das alterações
        db.session.commit()
        
        print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    setup_database()