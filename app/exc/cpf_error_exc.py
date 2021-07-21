import re

def CPFError(cpf, response):
    match = re.search(r'\d{3}\.?\d{3}\.?\d{3}\-?\d{2}', cpf)
    if not match:
        return {"error": "Invalid format CPF"}
    return response