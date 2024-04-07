from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFont
import ArrPro
import pyperclip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()     

        fonte = QFont()
        fonte.setPointSize(12) 

        self.label_personagens = QLabel("Personagens")
        self.label_quadros = QLabel("Quadros")
        self.label_saida = QLabel("Saída")
        self.input_text1 = QTextEdit(self)
        self.input_text2 = QTextEdit(self)
        self.process_button = QPushButton("Processar", self)
        self.process_button.clicked.connect(self.on_process_button_clicked)  # Conectar ao método de processamento        
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)  

        # Aplica a fonte aos widgets
        self.label_personagens.setFont(fonte)
        self.label_quadros.setFont(fonte)
        self.label_saida.setFont(fonte)
        self.input_text1.setFont(fonte)
        self.input_text2.setFont(fonte)
        self.output_text.setFont(fonte)

        layout = QVBoxLayout()
        layout.addWidget(self.label_personagens)
        layout.addWidget(self.input_text1)
        layout.addWidget(self.label_quadros)
        layout.addWidget(self.input_text2)
        layout.addWidget(self.process_button)  
        layout.addWidget(self.label_saida)
        layout.addWidget(self.output_text)        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Coloca os personagens nos quadros")
        self.setGeometry(150, 150, 600, 400)
        self.carregar_textos_iniciais()

    def carregar_textos_iniciais(self):
        try:
            with open('personagens.txt', 'r', encoding='ISO-8859-1') as f:
                self.input_text1.setPlainText(f.read())
        except FileNotFoundError:
            print("Arquivo 'personagens.txt' não encontrado. Iniciando com campo vazio.")
            self.input_text1.setPlainText("")
        try:
            with open('quadros.txt', 'r', encoding='ISO-8859-1') as f:
                self.input_text2.setPlainText(f.read())
        except FileNotFoundError:
            print("Arquivo 'quadros.txt' não encontrado. Iniciando com campo vazio.")
            self.input_text2.setPlainText("")        

    def on_process_button_clicked(self):
        with open('personagens.txt', 'w', encoding='ISO-8859-1') as f:
            f.write(self.input_text1.toPlainText())
        with open('quadros.txt', 'w', encoding='ISO-8859-1') as f:
            f.write(self.input_text2.toPlainText())        
        ArrPro.processar_dados()
        with open('saida.txt', 'r', encoding='ISO-8859-1') as f:
            saida = f.read()
        conteudo_utf8 = saida.encode('ISO-8859-1').decode('UTF-8')
        self.output_text.setPlainText(conteudo_utf8)

def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    main()
