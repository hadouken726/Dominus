import re

def validation(cpf, phone, response):

    match_cpf = re.search(r'^\d{11}$', cpf)
    match_phone = re.search(r"^(\++\d{2})?\d{11}", phone)

    if not match_cpf:
        return {"error": "Invalid format CPF, only numeric format accepted"}
    if not match_phone: 
        return {
            "error": "Invalid format Phone, number must be max of 11 characteres and country code is optional"
        }
    return response

