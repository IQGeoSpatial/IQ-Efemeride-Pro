
import os
import json
import sqlite3

def get_db_path(db_name="UsrMicrosoftIQQ.db"):
    """Obtiene la ruta a la base de datos en una carpeta segura del usuario."""
    app_data_dir = os.path.join(os.path.expanduser("~"), ".UsrMicrosoftIQQ")
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, db_name)

# --- LicenciaDB SQLite ---
class LicenciaDB:
    def __init__(self, db_name="UsrMicrosoftIQQ.db"):
        self.db_path = get_db_path(db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS licencia (
                    id INTEGER PRIMARY KEY,
                    usuario TEXT,
                    licencia TEXT,
                    expiracion TEXT,
                    usos INTEGER DEFAULT 0
                )
            """)
            # Asegurarse de que solo haya una fila de licencia
            cursor.execute("SELECT COUNT(*) FROM licencia WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO licencia (id, usuario, licencia) VALUES (1, '', '')")

    def guardar_licencia(self, usuario, licencia):
        with self.conn:
            self.conn.execute(
                "UPDATE licencia SET usuario = ?, licencia = ? WHERE id = 1",
                (usuario, licencia)
            )

    def cargar_licencia(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT usuario, licencia, expiracion FROM licencia WHERE id = 1")
            return cursor.fetchone()

    def registrar_uso(self):
        with self.conn:
            self.conn.execute("UPDATE licencia SET usos = usos + 1 WHERE id = 1")

    def obtener_usos(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT usos FROM licencia WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else 0

    def close(self):
        self.conn.close()

# --- CodigoDB SQLite ---
class CodigoDB:
    def __init__(self, db_name="UsrMicrosoftIQQ.db"):
        self.db_path = get_db_path(db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("CREATE TABLE IF NOT EXISTS codigos (codigo TEXT PRIMARY KEY, usado INTEGER DEFAULT 0)")

    def agregar_codigo(self, codigo):
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO codigos (codigo) VALUES (?)", (codigo,))

    def obtener_codigos(self):
        with self.conn:
            return self.conn.execute("SELECT codigo, usado FROM codigos ORDER BY codigo").fetchall()

    def eliminar_codigo(self, codigo):
        with self.conn:
            self.conn.execute("DELETE FROM codigos WHERE codigo = ?", (codigo,))

    def editar_codigo(self, codigo_antiguo, nuevo_codigo):
        with self.conn:
            self.conn.execute("UPDATE codigos SET codigo = ? WHERE codigo = ?", (nuevo_codigo, codigo_antiguo))

    def limpiar_codigos(self):
        with self.conn:
            self.conn.execute("DELETE FROM codigos")