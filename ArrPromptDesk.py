from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
import ArrPro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        # Criar os labels
        self.label_personagens = QLabel("Personagens")
        self.label_quadros = QLabel("Quadros")
        self.label_saida = QLabel("Saída")

        # Criar os campos de texto de entrada
        self.input_text1 = QTextEdit(self)
        self.input_text2 = QTextEdit(self)

        # Criar o botão de processamento
        self.process_button = QPushButton("Processar", self)
        self.process_button.clicked.connect(self.on_process_button_clicked)  # Conectar ao método de processamento        

        # Criar o campo de texto de saída
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)  # Torna o campo de saída somente leitura


        # Layout vertical para organizar os widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label_personagens)
        layout.addWidget(self.input_text1)
        layout.addWidget(self.label_quadros)
        layout.addWidget(self.input_text2)
        layout.addWidget(self.process_button)  
        layout.addWidget(self.label_saida)
        layout.addWidget(self.output_text)        

        # Configurar o widget central com o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Configurações adicionais da janela
        self.setWindowTitle("Programa com Botão de Processamento")
        self.setGeometry(100, 100, 400, 300)

        self.carregar_textos_iniciais()

    def carregar_textos_iniciais(self):
        # Carregar o conteúdo de 'personagens.txt' em input_text1
        try:
            with open('personagens.txt', 'r', encoding='utf-8') as f:
                self.input_text1.setPlainText(f.read())
        except FileNotFoundError:
            print("Arquivo 'personagens.txt' não encontrado. Iniciando com campo vazio.")
            self.input_text1.setPlainText("")

        # Carregar o conteúdo de 'quadros.txt' em input_text2
        try:
            with open('quadros.txt', 'r', encoding='utf-8') as f:
                self.input_text2.setPlainText(f.read())
        except FileNotFoundError:
            print("Arquivo 'quadros.txt' não encontrado. Iniciando com campo vazio.")
            self.input_text2.setPlainText("")        

    def on_process_button_clicked(self):
        # Salvar os textos nos arquivos correspondentes
        with open('personagens.txt', 'w', encoding='ISO-8859-1') as f:
            f.write(self.input_text1.toPlainText())
        with open('quadros.txt', 'w', encoding='ISO-8859-1') as f:
            f.write(self.input_text2.toPlainText())

        # Chamar a função de processamento do ArrPro.py
        ArrPro.processar_dados()

        # Ler a saída e mostrar no campo de saída
        with open('saida.txt', 'r', encoding='utf-8') as f:
            saida = f.read()
        self.output_text.setPlainText(saida)

def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    main()
