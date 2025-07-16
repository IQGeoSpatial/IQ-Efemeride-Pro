from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QRadialGradient, QColor, QPainterPath, QPen
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint, QRectF
import math

class PlasmaCircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)        
        self.setMinimumSize(120, 120)
        self.setMaximumSize(180, 180)
        self._pulse = 0.0
        self._pulse_increment = 0.05
        self._pulse_direction = 1.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(20)  # ~50 FPS para una animación más fluida

    def _animate(self):
        self._pulse += self._pulse_increment * self._pulse_direction

        # Invertir dirección y fijar en los límites para evitar que se pase
        if self._pulse >= 1.0:
            self._pulse = 1.0
            self._pulse_direction = -1.0
        elif self._pulse <= 0.0:
            self._pulse = 0.0
            self._pulse_direction = 1.0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        center = self.rect().center()
        # Reducir el radio máximo para evitar que la animación se corte en los bordes
        max_radius = min(self.width(), self.height()) * 0.25
        num_rings = 4
        num_points_per_ring = 120
        
        for i in range(num_rings):
            # --- Color individual para cada anillo ---
            # Base de color en turquesa/celeste (190) y se desplaza hacia azul/morado
            base_hue = 190 #190
            hue_offset = i * 25  # Cada anillo tiene un color diferente

            current_hue = (base_hue + hue_offset) % 360
            ring_color = QColor.fromHsvF(current_hue / 360.0, 0.85, 1.0)

            path = QPainterPath()
            
            # --- Propiedades de animación del anillo ---
            current_radius = max_radius * (0.5 + 0.5 * (i / (num_rings - 1)))
            amplitude = max_radius * 0.1 * (i + 1) * (0.5 + self._pulse * 1.5)
            frequency = 4 + i
            
            # --- Velocidad y dirección de rotación ---
            # Todas las líneas giran en la misma dirección
            # Las líneas exteriores son más lentas que las interiores
            speed_factor = - (1.0 - (i / num_rings) * 0.7)  # Negativo para antihorario
            phase_shift = self._pulse * math.pi * 2 * speed_factor

            for j in range(num_points_per_ring + 1):
                angle_rad = (j / num_points_per_ring) * 2 * math.pi
                
                # Perturbar el radio para crear una onda
                r = current_radius + amplitude * math.sin(frequency * angle_rad + phase_shift)
                x = center.x() + r * math.cos(angle_rad)
                y = center.y() + r * math.sin(angle_rad)
                if j == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            # --- Dibujado con efecto de brillo ---
            # 1. Brillo (línea gruesa y semitransparente)
            glow_color = QColor(ring_color)
            glow_alpha = int(80 * (1 - (i / num_rings)) * (0.5 + self._pulse))
            glow_color.setAlpha(glow_alpha)
            painter.setPen(QPen(glow_color, 3 + i * 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(path)

            # 2. Línea principal (más delgada y brillante)
            line_color = QColor(ring_color)
            line_color.setAlpha(230) # Ligeramente transparente para suavizar
            painter.setPen(QPen(line_color, 1.5))
            painter.drawPath(path)

        painter.end()
