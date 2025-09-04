#Here are the contents for the file `src/main.py`:

import sys
import os
import tempfile
import time

from PyQt5.QtWidgets import QApplication
from GUI.efemerides_dialog import EfemeridesDialog
from GUI.splash import SplashScreen
from GUI.themes import LIGHT_THEME
from utils.resource_path import resource_path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --- Fin de la solución ---


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
