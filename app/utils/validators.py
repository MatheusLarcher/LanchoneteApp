# app/utils/validators.py
import re

def validate_phone(phone):
    """
    Valida um número de telefone no formato brasileiro.
    Aceita formatos: XXXXXXXXXX, (XX)XXXXXXXX, (XX) XXXXXXXX, 
    XXXXXXXXXXX, (XX)XXXXXXXXX, (XX) XXXXXXXXX
    """
    # Remove caracteres não numéricos
    phone_digits = re.sub(r'\D', '', phone)
    
    # Verifica se o telefone tem entre 10 e 11 dígitos (com DDD)
    if len(phone_digits) < 10 or len(phone_digits) > 11:
        return False
    
    return True

def validate_required_fields(data, fields):
    """
    Valida se todos os campos obrigatórios foram preenchidos.
    Retorna uma lista com os nomes dos campos não preenchidos.
    """
    missing = []
    for field in fields:
        if field not in data or not data[field]:
            missing.append(field)
    return missing