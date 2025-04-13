# Aplicativo Web de Lanchonete com Flask

Um aplicativo web para o módulo cliente de uma lanchonete, desenvolvido com Flask e seguindo uma arquitetura limpa e modular. Este projeto implementa um cardápio digital interativo e um sistema de pedidos online.

## Funcionalidades

- **Cardápio Digital**: Navegação por categorias, busca e filtros de produtos
- **Carrinho de Compras**: Adição, remoção e atualização de itens
- **Checkout**: Finalização de pedidos com dados do cliente
- **Acompanhamento de Pedidos**: Visualização do status atual do pedido
- **Design Responsivo**: Layout adaptado para dispositivos móveis e desktop

## Tecnologias Utilizadas

- **Flask 2.x**: Framework web em Python
- **PostgreSQL**: Banco de dados relacional
- **SQLAlchemy**: ORM para mapear tabelas em classes Python
- **Bootstrap 5**: Framework CSS para design responsivo
- **HTML5, CSS3 e JavaScript**: Tecnologias front-end
- **Jinja2**: Sistema de templates do Flask

## Requisitos de Sistema

- Python 3.10+
- PostgreSQL
- Pip (gerenciador de pacotes Python)

## Estrutura do Projeto

```
/app
  /static
    /css        (arquivos CSS personalizados)
    /js         (arquivos JavaScript personalizados)
    /images     (imagens gerais do site, ex: logo)
    /produtos   (imagens dos produtos do cardápio)
  /templates
    /cliente    (templates HTML para o módulo cliente)
  /models       (modelos de dados SQLAlchemy)
  /controllers  (controllers e rotas)
  /utils        (funções auxiliares)
  __init__.py   (inicialização da aplicação Flask)
  config.py     (configurações da aplicação)
  routes.py     (registro de blueprints)
/migrations     (migrations do banco de dados)
/requirements.txt (dependências do projeto)
/run.py         (script para iniciar a aplicação)
/setup_db.py    (script para criar o banco e popular dados)
```

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/lanchonete-app.git
   cd lanchonete-app
   ```

2. Crie e ative um ambiente virtual Python:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:
   - Crie um banco de dados PostgreSQL
   - Edite as configurações de conexão em `app/config.py` ou defina a variável de ambiente `DATABASE_URL`

5. Execute o script para criar o banco de dados e popular com dados iniciais:
   ```bash
   python setup_db.py
   ```

6. Inicie a aplicação:
   ```bash
   python run.py
   ```

7. Acesse a aplicação no navegador: http://127.0.0.1:5000/

## Módulos e Funcionamento

### Cardápio Digital
- Navegação por categorias de produtos
- Visualização de produtos por categoria
- Detalhes de produtos individuais
- Filtros e ordenação de produtos

### Carrinho de Compras
- Adição de produtos ao carrinho
- Remoção de itens
- Atualização de quantidades
- Adição de observações por item

### Checkout
- Formulário de dados do cliente
- Escolha do tipo de pedido (Delivery, Retirada, Local)
- Seleção da forma de pagamento
- Resumo do pedido

### Acompanhamento de Pedido
- Visualização do status atual
- Detalhes do pedido
- Itens do pedido
- Atualização automática

## Desenvolvimento

Para contribuir com o projeto:

1. Crie um fork do repositório
2. Clone seu fork: `git clone https://github.com/MatheusLarcher/LanchoneteApp.git`
3. Crie uma branch para sua feature: `git checkout -b MatheusLarcher`
4. Faça suas alterações e commit: `git commit -m 'Minha nova feature'`
5. Envie para o GitHub: `git push origin MatheusLarcher`
6. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para dúvidas ou sugestões, entre em contato através do email: matheuslarcher20@gmail.com