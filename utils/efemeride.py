from datetime import datetime

def date_to_gps_week(dt):
    """Convierte un objeto datetime a la semana GPS y el día de la semana."""
    gps_epoch = datetime(1980, 1, 6)
    delta = dt - gps_epoch.date()
    total_days = delta.days
    gps_week = total_days // 7
    day_of_week = total_days % 7
    return gps_week, day_of_week

def date_to_julian_day(dt):
    """Calcula el Julian Day Number para una fecha dada."""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    jdn -= 1
    return f"{jdn}.5"

# Configuración unificada para GNSS y alias (todos los archivos en la misma carpeta, solo cambia el nombre del archivo)
FTP_CONFIG = {
    "COD": {
        "server": "spiftp.esac.esa.int",
        "path_template": "/gnss/products/{gps_week}",
        "interval": "05M"
    },
    "ESA": {
        "server": "spiftp.esac.esa.int",
        "path_template": "/gnss/products/{gps_week}",
        "interval": "05M"
    },
    "IGS": {
        "server": "spiftp.esac.esa.int",
        "path_template": "/gnss/products/{gps_week}",
        "interval": "15M"
    },
    "GFZ": {
        "server": "spiftp.esac.esa.int",
        "path_template": "/gnss/products/{gps_week}",
        "interval": "05M"
    },
    "WHU": {
        "server": "spiftp.esac.esa.int",
        "path_template": "/gnss/products/{gps_week}",
        "interval": "05M"
    }
}

# Configuración para diferentes tipos de productos de efemérides
EPHEM_TYPE_CONFIG = {
    "Ultra-rápido": {"code": "ULT", "duration": "02D"},
    "Rápido":       {"code": "RAP", "duration": "01D"},
    "Final":        {"code": "FIN", "duration": "01D"}
}
