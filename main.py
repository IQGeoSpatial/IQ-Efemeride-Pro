#Here are the contents for the file `src/main.py`:

import sys
import os

# --- Solución al ModuleNotFoundError ---
# Esta sección debe estar ANTES de cualquier importación de tu proyecto (GUI, utils, etc.)
# Añade el directorio raíz del proyecto (donde se encuentra este archivo main.py)
# a la ruta de búsqueda de Python. Esto asegura que los módulos como 'utils' y 'GUI'
# se encuentren siempre, tanto en desarrollo como en el ejecutable de PyInstaller.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --- Fin de la solución ---

from PyQt5.QtWidgets import QApplication
from GUI.efemerides_dialog import EfemeridesDialog
from GUI.splash import SplashScreen
from GUI.themes import LIGHT_THEME
from utils.resource_path import resource_path


import os
import tempfile
import time

def limpiar_temp(dias=1):
    """Limpia archivos temporales creados por esta aplicación que son más antiguos que 'dias'."""
    temp_dir = tempfile.gettempdir() # C:\Users\user\AppData\Local\Temp
    ahora = time.time()
    # Prefijos de archivos temporales usados por la aplicación
    prefijos_app = ("iq_", "recorte_", "mapa_temp")
    for nombre in os.listdir(temp_dir):
        if nombre.startswith(prefijos_app):
            ruta = os.path.join(temp_dir, nombre)
            try:
                # Comprobar si es un archivo y si es más antiguo que el límite
                if os.path.isfile(ruta) and (ahora - os.path.getmtime(ruta) > dias * 86400):
                    os.remove(ruta)
                # Opcional: limpiar también directorios temporales vacíos o antiguos
                elif os.path.isdir(ruta):
                    # Aquí se podría añadir lógica para limpiar directorios si es necesario
                    pass
            except Exception:
                # Ignorar errores si el archivo está en uso, etc.
                pass

# Llama a esta función al inicio
limpiar_temp(dias=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Aplicar tema claro por defecto, reemplazando el placeholder de la imagen
    bg_image_path = resource_path(os.path.join("Assets", "Image", "license_bg.jpg")).replace(os.sep, '/')
    app.setStyleSheet(LIGHT_THEME.replace("{bg_image_path}", bg_image_path))

    splash = SplashScreen()
    splash.show()
    app.processEvents()


    # Mantener referencia global
    global efem_dialog_instance
    efem_dialog_instance = None

    def show_main():
        global efem_dialog_instance
        print("Abriendo ventana principal... (antes de crear EfemeridesDialog)")
        try:
            efem_dialog_instance = EfemeridesDialog()
            print("EfemeridesDialog creado correctamente")
            efem_dialog_instance.show()
            print("show() ejecutado")
        except Exception as e:
            print(f"Error al crear o mostrar EfemeridesDialog: {e}")

    splash.start(show_main)
    sys.exit(app.exec_())

#pyinstaller --noconfirm --onefile --windowed --icon=Assets\Icono\icono.ico --add-data "Assets;Assets" main.py
#para poner instalador
# pyinstaller --noconfirm --windowed --icon=Assets\Icono\icono.ico --add-data "Assets;Assets" main.py