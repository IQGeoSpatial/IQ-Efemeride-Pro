import sys
import os

def resource_path(relative_path):
    """
    Devuelve la ruta absoluta de un recurso, compatible con PyInstaller y desarrollo.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        # Usar SIEMPRE la raíz del proyecto, no la carpeta de utils ni el script actual
        # Busca la carpeta que contiene main.py
        current = os.path.abspath(os.path.dirname(__file__))
        while True:
            if os.path.exists(os.path.join(current, 'main.py')):
                base_path = current
                break   
            parent = os.path.dirname(current)
            if parent == current:
                # Llegamos a la raíz del disco y no encontramos main.py
                base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
                break
            current = parent
    return os.path.join(base_path, relative_path)