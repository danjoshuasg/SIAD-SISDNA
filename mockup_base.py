import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Usuario')
        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Contraseña')
        self.password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Iniciar sesión', self)
        login_button.clicked.connect(self.login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        self.setLayout(layout)
        self.setWindowTitle('Inicio de sesión')
        self.show()

    def login(self):
        # Aquí iría la lógica de autenticación
        if self.username.text() == 'admin' and self.password.text() == 'password':
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            print("Credenciales incorrectas")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        load_button = QPushButton('Cargar archivo', self)
        load_button.clicked.connect(self.load_file)
        self.file_label = QLabel('Ningún archivo seleccionado', self)
        automate_button = QPushButton('Automatizar', self)
        automate_button.clicked.connect(self.automate)

        layout.addWidget(load_button)
        layout.addWidget(self.file_label)
        layout.addWidget(automate_button)
        self.setLayout(layout)
        self.setWindowTitle('Ventana Principal')
        self.show()

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Excel Files (*.xlsx);;JSON Files (*.json);;Text Files (*.txt)")
        if file_name:
            self.file_label.setText(f'Archivo cargado: {file_name}')
            # Aquí puedes agregar la lógica para leer el archivo
            if file_name.endswith('.xlsx'):
                df = pd.read_excel(file_name)
            elif file_name.endswith('.json'):
                df = pd.read_json(file_name)
            elif file_name.endswith('.txt'):
                df = pd.read_csv(file_name, sep='\t')
            print(df.head())  # Muestra las primeras filas del DataFrame

    def automate(self):
        # Configuración de Selenium
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            # Ejemplo de automatización: abrir Google y realizar una búsqueda
            driver.get("https://www.google.com")
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("Python automation")
            search_box.send_keys(Keys.RETURN)
            print("Búsqueda realizada con éxito")
        finally:
            driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    sys.exit(app.exec_())