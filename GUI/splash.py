import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
from utils.resource_path import resource_path

class SplashScreen(QWidget):

    """
    Una pantalla de bienvenida personalizada con una imagen de fondo y barra de progreso.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(700, 480) # Más ancho
        # Fondo con la imagen portada.jpeg
        portada_path = resource_path(os.path.join("Assets", "Image", "portada.jpeg"))
        self._portada_pixmap = QPixmap(portada_path)
        self.setStyleSheet("")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.addStretch(2)
        layout.addSpacing(20)

        # Etiqueta de estado
        self.status_label = QLabel("Cargando componentes de IQ GeoSpatial...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold; background: transparent; text-shadow: 1px 1px 4px #000;")
        layout.addWidget(self.status_label)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        layout.addStretch(1) # Añade menos espacio flexible en la parte inferior

        self.progress_value = 0
        self.timer = QTimer(self)

    def paintEvent(self, event):
        # Pintar la imagen de portada como fondo
        if hasattr(self, '_portada_pixmap') and not self._portada_pixmap.isNull():
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self._portada_pixmap)
        else:
            super().paintEvent(event)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #888;
                border-radius: 8px;
                text-align: center;
                background-color: rgba(0, 0, 0, 150);
                color: white;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 8px;
            }
        """)

    def start(self, callback, duration=2500):
        """
        Muestra el splash screen y simula el progreso.
        """
        self.show()
        self.timer.timeout.connect(lambda: self.update_progress(callback))
        # El intervalo del timer define la "suavidad" de la barra
        self.timer.start(duration // 100)

    def update_progress(self, callback):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.finish_splash(callback)

    def finish_splash(self, callback):
        """
        Cierra el splash screen y muestra la ventana principal.
        """
        callback()
        self.close()