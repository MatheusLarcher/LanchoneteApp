# app/utils/helpers.py
from decimal import Decimal

def format_currency(value):
    """Formata um valor numérico para o formato de moeda brasileira (R$)."""
    if isinstance(value, str):
        try:
            value = Decimal(value)
        except:
            return value
    
    if isinstance(value, (int, float, Decimal)):
        return f'R$ {value:.2f}'.replace('.', ',')
    
    return value

def calculate_subtotal(preco, quantidade):
    """Calcula o subtotal de um item (preço unitário x quantidade)."""
    try:
        return Decimal(preco) * int(quantidade)
    except:
        return 0

def calculate_total(items):
    """Calcula o total de uma lista de itens no carrinho."""
    total = 0
    for item in items.values():
        subtotal = calculate_subtotal(item['preco_unit'], item['quantidade'])
        total += subtotal
    return total