# app/config.py
import os
from urllib.parse import quote
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'minha_chave_secreta_para_lanchonete')
    senha = quote(os.environ.get('senha_postgres'))
    ip_postgres = os.environ.get('ip_postgres')

    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{senha}@{ip_postgres}:5001/lanchonete'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações adicionais
    UPLOAD_FOLDER = os.path.join('app', 'static', 'produtos')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}