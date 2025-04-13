# app/routes.py
from flask import render_template

def init_routes(app):
    # Registrar blueprint do cliente
    from app.controllers.cliente_controller import cliente_bp
    app.register_blueprint(cliente_bp, url_prefix='/')
    
    # Tratamento de erros
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('cliente/error.html', error="Página não encontrada", code=404), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('cliente/error.html', error="Erro interno do servidor", code=500), 500