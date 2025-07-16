HASH_USOS_SECRET = "&IQ20#&25Geo%&Spatial#06/%08_HASH_USOS"

def hash_usos(valor):
    texto = f"{valor}{HASH_USOS_SECRET}"
    return hashlib.sha256(texto.encode()).hexdigest()
import hashlib
import uuid
from Models.DataBase import LicenciaDB

CLAVE_SECRETA = "&IQ20#&25Geo%&Spatial#06/%08"

def obtener_mac():
    return str(uuid.getnode())

def generar_licencia(nombre_usuario, mac, clave_secreta=CLAVE_SECRETA):
    # Sufijo exclusivo para este proyecto
    proyecto_id = "EFEM2025"  # Cambia esto si quieres otro identificador
    texto = nombre_usuario + mac + clave_secreta + proyecto_id
    raw_key = hashlib.sha256(texto.encode()).hexdigest()[:36]  # 36 caracteres
    formatted_key = '-'.join(raw_key[i:i+4] for i in range(0, len(raw_key), 4)).upper()
    return formatted_key

def validar_licencia(nombre_usuario, licencia_ingresada, clave_secreta=CLAVE_SECRETA):
    mac = obtener_mac()
    licencia_valida = generar_licencia(nombre_usuario, mac, clave_secreta)
    return licencia_ingresada.upper() == licencia_valida

def cargar_estado():
    db = LicenciaDB()
    licencia_data = db.cargar_licencia()
    usos = db.obtener_usos()
    usos_hash = db.obtener_usos_hash() if hasattr(db, 'obtener_usos_hash') else None
    db.close()
    # Validar hash si existe
    if usos_hash is not None:
        if hash_usos(usos) != usos_hash:
            return {"descargas": 99, "licencia": "", "usuario": ""}  # Valor manipulado, fuerza bsloqueo
    if licencia_data:
        usuario, licencia, _ = licencia_data
        return {"descargas": usos, "licencia": licencia or "", "usuario": usuario or ""}
    return {"descargas": 0, "licencia": "", "usuario": ""}

def guardar_estado(estado):
    pass

def puede_usar_app():
    estado = cargar_estado()
    if estado.get("licencia"):
        nombre_usuario = estado.get("usuario", "")
        if validar_licencia(nombre_usuario, estado["licencia"]):
            return True
        else:
            return False
    if estado["descargas"] < 2:  # Límite de 1 uso gratuito. Si usos=0, permite. Si usos=1, bloquea.
        return True
    else:
        return False

def registrar_uso():
    estado = cargar_estado()
    if not estado.get("licencia"):
        db = LicenciaDB()
        db.registrar_uso()
        # Guardar hash actualizado si la función existe
        if hasattr(db, 'guardar_usos_hash'):
            usos = db.obtener_usos()
            db.guardar_usos_hash(hash_usos(usos))
        db.close()

def ingresar_licencia(nombre_usuario, licencia):
    if validar_licencia(nombre_usuario, licencia):
        db = LicenciaDB()
        db.guardar_licencia(nombre_usuario, licencia)
        db.close()
        return True
    else:
        return False