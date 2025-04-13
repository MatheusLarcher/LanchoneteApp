# app/controllers/cliente_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.forma_pagamento import FormaPagamento
from app.models.pedido import Pedido, TipoPedido, StatusPedido
from app.models.item_pedido import ItemPedido
from app.utils.helpers import calculate_total
from app.utils.validators import validate_phone, validate_required_fields
from datetime import datetime
from decimal import Decimal

# Criação do blueprint para o módulo cliente
cliente_bp = Blueprint('cliente', __name__, template_folder='../templates/cliente')

# Rota principal - página inicial
@cliente_bp.route('/')
def index():
    # Consultar categorias ordenando pela coluna 'ordem'
    categorias = Categoria.query.order_by(Categoria.ordem).all()
    # Consultar produtos em destaque e disponíveis
    destaques = Produto.query.filter_by(destaque=True, status=True).all()
    return render_template('cliente/index.html', categorias=categorias, destaques=destaques)

# Rota para listar todas as categorias
@cliente_bp.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.order_by(Categoria.ordem).all()
    return render_template('cliente/categorias.html', categorias=categorias)

# Rota para listar produtos de uma categoria
@cliente_bp.route('/categoria/<int:categoria_id>')
def produtos_por_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    
    # Base query: produtos da categoria, disponíveis
    query = Produto.query.filter_by(categoria_id=categoria.id, status=True)
    
    # Aplicar filtros se parâmetros presentes
    search = request.args.get('buscar')
    ordenar = request.args.get('ordenar')
    
    if search:
        query = query.filter(Produto.nome.ilike(f'%{search}%'))
    
    if ordenar == 'preco':
        query = query.order_by(Produto.preco)
    elif ordenar == 'nome':
        query = query.order_by(Produto.nome)
    elif ordenar == 'preco_desc':
        query = query.order_by(Produto.preco.desc())
    
    produtos = query.all()
    
    return render_template(
        'cliente/produtos.html', 
        categoria=categoria, 
        produtos=produtos, 
        buscar=search, 
        ordenar=ordenar
    )

# Rota para exibir detalhes de um produto
@cliente_bp.route('/produto/<int:produto_id>')
def detalhar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    # Verificar se o produto está disponível
    if not produto.status:
        flash('Produto indisponível no momento.', 'warning')
        return redirect(url_for('cliente.produtos_por_categoria', categoria_id=produto.categoria_id))
    
    return render_template('cliente/produto_detalhe.html', produto=produto)

# Rota para adicionar produto ao carrinho
@cliente_bp.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if not produto.status:
        flash('Produto indisponível, não pode ser adicionado.', 'error')
        return redirect(url_for('cliente.index'))
    
    quantidade = int(request.form.get('quantidade', 1))
    observacoes = request.form.get('observacoes', '')
    
    # Inicializar carrinho na sessão se não existir
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    carrinho = session['carrinho']
    
    # Se produto já estiver no carrinho, soma as quantidades
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]['quantidade'] += quantidade
        # Atualizar observações se fornecidas
        if observacoes:
            carrinho[str(produto_id)]['obs'] = observacoes
    else:
        # Adiciona novo item ao carrinho
        carrinho[str(produto_id)] = {
            'nome': produto.nome,
            'quantidade': quantidade,
            'preco_unit': float(produto.preco),
            'obs': observacoes
        }
    
    session.modified = True  # informa ao Flask que a sessão foi alterada
    flash(f'Adicionado {quantidade}x {produto.nome} ao carrinho.', 'success')
    
    return redirect(url_for('cliente.ver_carrinho'))

# Rota para visualizar o carrinho
@cliente_bp.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', {})
    
    # Calcular total geral
    total = calculate_total(carrinho)
    
    return render_template('cliente/carrinho.html', carrinho=carrinho, total=total)

# Rota para remover item do carrinho
@cliente_bp.route('/carrinho/remover/<produto_id>')
def remover_item_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    
    if str(produto_id) in carrinho:
        produto_nome = carrinho[str(produto_id)]['nome']
        del carrinho[str(produto_id)]
        session.modified = True
        flash(f'Removido {produto_nome} do carrinho.', 'info')
    
    return redirect(url_for('cliente.ver_carrinho'))

# Rota para atualizar quantidades no carrinho
@cliente_bp.route('/carrinho/atualizar', methods=['POST'])
def atualizar_carrinho():
    carrinho = session.get('carrinho', {})
    
    for produto_id, data in carrinho.items():
        nova_qtd = int(request.form.get(f'quantidade_{produto_id}', data['quantidade']))
        data['quantidade'] = nova_qtd if nova_qtd > 0 else 1
        
        # Atualizar observações se houver campo
        nova_obs = request.form.get(f'observacoes_{produto_id}', data.get('obs', ''))
        data['obs'] = nova_obs
    
    session.modified = True
    flash('Carrinho atualizado.', 'success')
    
    return redirect(url_for('cliente.ver_carrinho'))

# Rota para a página de checkout
@cliente_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    carrinho = session.get('carrinho', {})
    
    if not carrinho:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('cliente.index'))
    
    if request.method == 'GET':
        # Obter formas de pagamento para listar no form
        formas = FormaPagamento.query.all()
        return render_template('cliente/checkout.html', carrinho=carrinho, formas_pag=formas)
    
    # Se for POST, processar dados do form
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo_pedido')  # 'delivery', 'retirada' ou 'local'
    endereco = request.form.get('endereco')
    forma_id = request.form.get('forma_pagamento')
    
    # Validações básicas
    errors = []
    if not nome or not telefone or not tipo:
        errors.append("Por favor, preencha todos os campos obrigatórios.")
    
    # Se delivery, endereço é obrigatório
    if tipo == 'delivery' and not endereco:
        errors.append("Endereço é obrigatório para entrega.")
    
    # Validar formato do telefone
    if telefone and not validate_phone(telefone):
        errors.append("Formato do telefone inválido. Use (XX) XXXXX-XXXX ou XXXXXXXXXXX.")
    
    if errors:
        for err in errors:
            flash(err, 'error')
        
        # Re-exibir o formulário com os dados preenchidos
        formas = FormaPagamento.query.all()
        return render_template(
            'cliente/checkout.html', 
            carrinho=carrinho, 
            formas_pag=formas,
            nome=nome, 
            telefone=telefone, 
            tipo=tipo, 
            endereco=endereco, 
            forma_id=forma_id
        )
    
    # Se passou na validação, criar novo Pedido
    novo_pedido = Pedido(
        nome_cliente=nome,
        telefone=telefone,
        endereco=endereco if tipo == 'delivery' else None,
        tipo=TipoPedido(tipo),  # converte string para enum TipoPedido
        status=StatusPedido.PENDENTE,
        data_hora=datetime.now(),
        forma_pagamento_id=int(forma_id) if forma_id else None
    )
    
    db.session.add(novo_pedido)
    db.session.flush()  # obtém ID do pedido gerado
    
    # Criar ItemPedido para cada item no carrinho
    for prod_id, item in carrinho.items():
        produto_id = int(prod_id)
        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=produto_id,
            quantidade=item['quantidade'],
            preco_unitario=item['preco_unit'],
            observacoes=item.get('obs', '')
        )
        db.session.add(novo_item)
    
    db.session.commit()
    
    # Limpar carrinho da sessão após finalizar pedido
    session.pop('carrinho', None)
    
    # Redirecionar para página de confirmação
    return redirect(url_for('cliente.pedido_confirmado', pedido_id=novo_pedido.id))

# Rota para confirmação de pedido
@cliente_bp.route('/pedido_confirmado/<int:pedido_id>')
def pedido_confirmado(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('cliente/pedido_confirmado.html', pedido=pedido)

# Rota para acompanhamento de pedido
@cliente_bp.route('/acompanhar_pedido/<int:pedido_id>')
def acompanhar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('cliente/acompanhar_pedido.html', pedido=pedido)

# Rota para busca de acompanhamento por número e telefone
@cliente_bp.route('/buscar_pedido', methods=['GET', 'POST'])
def buscar_pedido():
    if request.method == 'POST':
        numero_pedido = request.form.get('numero_pedido')
        telefone = request.form.get('telefone')
        
        if not numero_pedido or not telefone:
            flash('Por favor, informe o número do pedido e o telefone.', 'warning')
            return render_template('cliente/buscar_pedido.html')
        
        try:
            # Buscar pedido pelo ID e telefone
            pedido = Pedido.query.filter_by(id=int(numero_pedido), telefone=telefone).first()
            
            if pedido:
                return redirect(url_for('cliente.acompanhar_pedido', pedido_id=pedido.id))
            else:
                flash('Pedido não encontrado com os dados fornecidos.', 'error')
        except:
            flash('Número de pedido inválido.', 'error')
    
    return render_template('cliente/buscar_pedido.html')