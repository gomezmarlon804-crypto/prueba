import hashlib
import hmac
import secrets


ITERACIONES_HASH = 310_000


def proteger_clave(clave):
    sal = secrets.token_hex(16)
    resumen = hashlib.pbkdf2_hmac(
        "sha256", clave.encode("utf-8"), bytes.fromhex(sal), ITERACIONES_HASH
    ).hex()
    return f"pbkdf2_sha256${ITERACIONES_HASH}${sal}${resumen}"


def verificar_clave(clave, clave_protegida):
    try:
        algoritmo, iteraciones, sal, resumen_esperado = clave_protegida.split("$")
        if algoritmo != "pbkdf2_sha256" or int(iteraciones) != ITERACIONES_HASH:
            return False
        resumen = hashlib.pbkdf2_hmac(
            "sha256",
            clave.encode("utf-8"),
            bytes.fromhex(sal),
            ITERACIONES_HASH,
        ).hex()
    except (AttributeError, ValueError, TypeError):
        return False
    return hmac.compare_digest(resumen, resumen_esperado)
