import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDialogButtonBox, QWidget, QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from utils.resource_path import resource_path
from utils.licencia_utils import ingresar_licencia, validar_licencia
from Models.DataBase import LicenciaDB
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class LicenciaDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activación de Licencia")
        self.setMinimumWidth(450)
        self.setObjectName("LicenciaDialog")

        logo_path = resource_path(os.path.join("Assets", "Image", "licencia.png"))
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Contenedor para aplicar estilos
        container = QWidget()
        container.setObjectName("Container")
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        title = QLabel("Activación del Producto")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)

        info_widget = QWidget()
        info_widget.setFixedWidth(320)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
                min-width: 220px;
                max-width: 340px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setSpacing(10)

        # Logo principal
        logo_label = QLabel()
        logo_path_main = resource_path(os.path.join("Assets", "Icon", "icono.ico"))
        if os.path.exists(logo_path_main):
            pixmap = QPixmap(logo_path_main).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedSize(90, 90)
        info_layout.addWidget(logo_label)

        # Texto de información (sin contacto, con precio)
        info_text = QLabel(
            "<b>IQ Efeméride Pro</b><br>"
            "Versión: 2.00.0<br>"
            #"<span style='color:#16a085;font-weight:bold;'>Precio: 50 Soles</span>"
        )
        info_text.setAlignment(Qt.AlignCenter)
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        # Labels de estado (ahora parte del widget que sí se muestra)
        self.estado_label = QLabel("Estado: Licencia pendiente de activación")
        self.estado_label.setAlignment(Qt.AlignCenter)
        self.estado_label.setStyleSheet("font-size: 12px; color: #3498db; font-weight: bold;")
        info_layout.addWidget(self.estado_label)

        self.exp_label = QLabel("Expira: Indefinida")
        self.exp_label.setAlignment(Qt.AlignCenter)
        self.exp_label.setStyleSheet("font-size: 12px; color: #e67e22;")
        info_layout.addWidget(self.exp_label)

        self.user_label = QLabel("Usuario: -")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("font-size: 12px; color: #16a085;")
        info_layout.addWidget(self.user_label)

        # self.code_label = QLabel("Licencia: -")
        # self.code_label.setAlignment(Qt.AlignCenter)
        # self.code_label.setStyleSheet("font-size: 12px; color: #8e44ad;")
        # info_layout.addWidget(self.code_label)
        
        layout.addWidget(info_widget, alignment=Qt.AlignCenter)

        # --- Botón Activar ---
        self.btn_activar = QPushButton("Activar")
        self.btn_activar.setStyleSheet("background: #3498db; color: white; border: none; border-radius: 5px; font-size: 13px; font-weight: bold; padding: 8px 24px;")
        layout.addWidget(self.btn_activar, alignment=Qt.AlignCenter)

        # --- Botón Solicitar Licencia ---
        self.btn_solicitar = QPushButton("Solicitar Licencia")
        self.btn_solicitar.setStyleSheet("background: #e67e22; color: white; border: none; border-radius: 5px; font-size: 13px; font-weight: bold; padding: 8px 24px;")
        self.btn_solicitar.hide()
        layout.addWidget(self.btn_solicitar, alignment=Qt.AlignCenter)

        # --- Campos ocultos hasta hacer clic en Activar ---
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Nombre completo registrado")
        self.user_input.hide()
        layout.addWidget(self.user_input)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX")
        self.key_input.hide()
        layout.addWidget(self.key_input)

        # Botones OK/Cancel ocultos hasta activar
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.hide()
        layout.addWidget(self.button_box)

        main_layout.addWidget(container)

        # Conectar el botón activar
        self.btn_activar.clicked.connect(self.mostrar_campos_activacion)
        self.btn_solicitar.clicked.connect(self.mostrar_formulario_solicitud)

        # Cargar estado de licencia al iniciar
        self.cargar_licencia_guardada()

    def cargar_licencia_guardada(self):
        db = LicenciaDB()
        licencia_data = db.cargar_licencia()
        db.close()

        if licencia_data:
            usuario, licencia, _ = licencia_data
            if usuario and licencia and validar_licencia(usuario, licencia):
                self.estado_label.setText("Estado: Activada")
                self.estado_label.setStyleSheet("font-size: 12px; color: #27ae60; font-weight: bold;")
                self.user_label.setText(f"Usuario: {usuario}")
                # self.code_label.setText(f"Licencia: {licencia}")

                # Ocultar campos de activación
                self.btn_activar.hide()

    def mostrar_campos_activacion(self):
        self.user_input.show()
        self.key_input.show()
        self.button_box.show()
        self.btn_activar.hide()
        self.btn_solicitar.show()
    def mostrar_formulario_solicitud(self):
        dialog = SolicitudLicenciaDialog(self)
        dialog.exec_()

    def get_datos(self):
        """Devuelve el nombre de usuario y la licencia ingresados."""
        return self.user_input.text().strip(), self.key_input.text().strip()
    
    def accept(self):
        nombre = self.user_input.text().strip()
        licencia = self.key_input.text().strip()
        if not nombre or not licencia:
            QMessageBox.warning(self, "Campos requeridos", "Debes ingresar el nombre y la licencia.")
            return

        if ingresar_licencia(nombre, licencia):
            # Actualiza los labels y la tarjeta con la información de licencia
            self.estado_label.setText("Estado: Activada")
            self.estado_label.setStyleSheet("font-size: 12px; color: #27ae60; font-weight: bold;")
            self.user_label.setText(f"Usuario: {nombre}")
            QMessageBox.information(self, "Licencia activada", "¡La licencia se ha activado correctamente!")
            # Acepta el diálogo para que la ventana que lo llamó sepa que fue exitoso.
            super().accept()
        else:
            QMessageBox.critical(self, "Licencia inválida", "La licencia ingresada no es válida para este equipo.")
            # No cerrar el diálogo ni la app

    def reject(self):
        # Solo cerrar el diálogo, nunca la app principal
        super().reject()

# --- Formulario de Solicitud de Licencia ---
class SolicitudLicenciaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Solicitar Licencia")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background: #f8f8f8;
                border-radius: 12px;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                margin-bottom: 10px;
                background: #fff;
            }
            QPushButton {
                background: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px 0px;
                margin-top: 12px;
            }
            QPushButton:hover {
                background: #219150;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre y Apellido")
        layout.addWidget(self.nombre_input)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.correo_input)

        self.whatsapp_input = QLineEdit()
        self.whatsapp_input.setPlaceholderText("Número de WhatsApp")
        layout.addWidget(self.whatsapp_input)

        self.asunto_input = QLineEdit()
        self.asunto_input.setPlaceholderText("Asunto (opcional)")
        layout.addWidget(self.asunto_input)

        self.mensaje_input = QLineEdit()
        self.mensaje_input.setPlaceholderText("Mensaje (opcional)")
        layout.addWidget(self.mensaje_input)

        self.btn_enviar = QPushButton("Enviar Solicitud")
        self.btn_enviar.setStyleSheet("background: #27ae60; color: white; font-weight: bold; border-radius: 5px; padding: 8px 24px;")
        self.btn_enviar.clicked.connect(self.enviar_solicitud)
        layout.addWidget(self.btn_enviar, alignment=Qt.AlignCenter)

    def enviar_solicitud(self):
        # Configura aquí tu correo y contraseña de aplicación
        remitente = "iqgeospatial@gmail.com"  # <-- Cambia esto por tu correo
        password = "llvc ubgz oipr izmp"  # <-- Cambia esto por tu contraseña de aplicación
        destinatario = remitente  # Puedes cambiarlo si quieres recibir en otro correo
        # Mensaje personalizado y profesional
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        whatsapp = self.whatsapp_input.text().strip()
        asunto = self.asunto_input.text().strip()
        mensaje = self.mensaje_input.text().strip()
        import re
        if not nombre or not correo or not whatsapp:
            QMessageBox.warning(self, "Campos requeridos", "Completa nombre, correo y número de WhatsApp.")
            return
        # Validar correo
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(email_regex, correo):
            QMessageBox.warning(self, "Correo inválido", "Ingresa un correo electrónico válido.")
            return
        # Validar número de WhatsApp (solo dígitos, mínimo 8)
        if not whatsapp.isdigit() or len(whatsapp) < 8:
            QMessageBox.warning(self, "WhatsApp inválido", "Ingresa un número de WhatsApp válido (solo dígitos, mínimo 8).")
            return
        import uuid
        mac = str(uuid.getnode())
        # Construir mensaje HTML con logo
        from email.mime.image import MIMEImage
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'Assets', 'Image', 'LOGO2.png')
        logo_path = os.path.abspath(logo_path)
        cuerpo_html = f'''
        <html>
        <body style="font-family: Arial, sans-serif; color: #222;">
            <p>Estimado Administrador,</p>
            <p>Se ha recibido una nueva solicitud de licencia para <b>IQ Efeméride Pro</b>.</p>
            <h4>Datos del solicitante:</h4>
            <table style="border-collapse:collapse;">
                <tr><td><b>Nombre completo:</b></td><td>{nombre}</td></tr>
                <tr><td><b>Correo electrónico:</b></td><td>{correo}</td></tr>
                <tr><td><b>WhatsApp:</b></td><td>{whatsapp}</td></tr>
                <tr><td><b>Asunto:</b></td><td>{asunto if asunto else '-'}</td></tr>
                <tr><td style="vertical-align:top;"><b>Mensaje:</b></td><td>{mensaje if mensaje else '-'}</td></tr>
                <tr><td><b>MAC del equipo:</b></td><td>{mac}</td></tr>
            </table>
            <p style="margin-top:24px;">Por favor, revise la información y proceda con la generación de la licencia si corresponde.</p>
            <br>
            <div style="text-align:center; margin-top:32px;">
                <img src="cid:logoimg" width="180" alt="Logo IQ GeoSpatial"/><br>
                <span style="font-size:13px;color:#888;">IQ GeoSpatial Pro</span>
            </div>
        </body>
        </html>
        '''
        msg = MIMEMultipart('related')
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = f"Solicitud de Licencia IQ Efeméride Pro - {nombre}"
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(cuerpo_html, 'html'))
        # Adjuntar logo embebido
        try:
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            image = MIMEImage(logo_data)
            image.add_header('Content-ID', '<logoimg>')
            image.add_header('Content-Disposition', 'inline', filename='logo.png')
            msg.attach(image)
        except Exception as e:
            pass  # Si no se encuentra el logo, simplemente no lo adjunta
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
            server.quit()
            QMessageBox.information(self, "Enviado", "La solicitud se envió correctamente. Pronto recibirá respuesta por correo.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo enviar el correo.\n{e}")
