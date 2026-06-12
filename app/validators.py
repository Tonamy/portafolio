import re


def validar_telefono(numero: str) -> bool:
    return bool(
        re.match(r'^\+?(\d[\d-. ]+)?(\(\d{3}\))?[\d-. ]{7,15}$', numero.replace(" ", ""))
    )


def validar_correo(correo: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo))