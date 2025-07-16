# Tema claro mínimo para la app de efemérides
LIGHT_THEME = '''
QDialog, QWidget {
    background-color: #f0f0f0;
}
QLabel {
    color: #333;
    background: transparent;
}
QPushButton {
    background: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 12px;
    font-weight: bold;
    padding: 8px;
}
QPushButton:disabled {
    background: #b0b0b0;
    color: #fff;
}
QProgressBar {
    border: 1px solid #bbb;
    border-radius: 5px;
    background: #e0e0e0;
    height: 18px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 5px;
}
'''
