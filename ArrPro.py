import re
import sys

primeira_chamada_log = True

class Personagem:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        split_descricao = descricao.split("Seed: ")
        if len(split_descricao) > 1:
            self.seed = split_descricao[1]
        else:
            self.seed = None
      
class Quadro:
   def __init__(self, estilo, descricao, personagens, descricao_completa):
       self.estilo = estilo
       self.descricao = descricao
       self.personagens = personagens
       self.descricao_completa = descricao_completa

def extrair_personagens_do_quadro(linha, personagens_dict):
    personagens_quadro = []
    if 'Personagens:' in linha:
        nomes_personagens = linha.split(':')[1].split(',')
        for nome in nomes_personagens:
            nome_limpo = nome.strip()
            if nome_limpo in personagens_dict:
                personagens_quadro.append(personagens_dict[nome_limpo])
    return personagens_quadro

def processar_quadros(entrada_quadros, personagens):
    log("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        log("Nenhum quadro encontrado no arquivo.")
        return quadros

    quadros_texto = entrada_quadros.split("Desenhe o ")[1:]  # Ignora a primeira parte vazia
    log(f"Total de quadros identificados: {len(quadros_texto)}")

    for quadro_texto in quadros_texto:
        linhas = quadro_texto.strip().split('\n')
        estilo, personagens_quadro, descricao = None, [], None

        for i, linha in enumerate(linhas):
            log(f"Linha processada: {linha}")
            if not estilo:
                estilo = processar_estilo(linha)
            if not personagens_quadro:
                personagens_quadro = extrair_personagens_do_quadro(linha, personagens)
            if not descricao and personagens_quadro:
                descricao = processar_descricao(linhas, i)

        if estilo and descricao:
            descricao_completa = f"Desenhe o Quadro no estilo {estilo}.\n{descricao}\n"
            for p in personagens_quadro:
                descricao_completa += f"{p.nome}: {p.descricao}\n"
            quadro = Quadro(estilo, descricao, personagens_quadro, descricao_completa)
            quadros.append(quadro)
            log(f"Quadro processado com sucesso.")
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")
            log(quadro_texto)
            sys.exit(1)

    return quadros

def processar_estilo(linha):
    if 'no estilo' in linha:
        estilo = linha.split('no estilo')[1].strip()
        return estilo
    return None

def processar_personagens(entrada_personagens):
    personagens = {}
    if not entrada_personagens.strip():
        return personagens
    for linha in entrada_personagens.split('\n'):
        match = re.match(r"([^:]+): (.+)", linha.strip())
        if match:
            nome, descricao = match.groups()
            personagens[nome] = Personagem(nome, descricao)
    return personagens

def processar_descricao(linhas, index):
    # A descrição começa na linha seguinte após "Personagens:"
    if index < len(linhas) - 1:
        return linhas[index + 1].strip()
    return None

def encontrar_personagens(nomes_personagens, personagens):
    personagens_encontrados = []
    for nome in nomes_personagens:
        nome = nome.strip()
        correspondencia_encontrada = False
        for chave, p in personagens.items():
            nome_personagem = chave.split(",")[0].strip()
            log(f"Comparando '{nome}' com '{nome_personagem}'")  # Debug
            if nome == nome_personagem:
                personagens_encontrados.append(p)
                correspondencia_encontrada = True
                log(f"Correspondência encontrada para '{nome}': {p.descricao}")  # Debug
                break  # Pára a busca assim que encontrar uma correspondência
        if not correspondencia_encontrada:
            log(f"Inconsistência nos personagens: '{nome}' não encontrado.")
            sys.exit(1)
    return personagens_encontrados

def gerar_saida(quadros):
    saida = ""
    for i, quadro in enumerate(quadros):
        saida += quadro.descricao_completa
        if i < len(quadros) - 1:  # Verifica se não é o último quadro
            saida += "\n"  # Adiciona duas linhas em branco para separar os quadros
    return saida.rstrip()  # Remove espaços em branco extras no final

def log(mensagem):
    global primeira_chamada_log
    modo = 'w' if primeira_chamada_log else 'a'
    with open("log.txt", modo) as arquivo_log:
        arquivo_log.write(mensagem + "\n")
    primeira_chamada_log = False

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return ""
    
def processar_dados():
    log("Lendo entradas")
    entrada_personagens = ler_arquivo(nome_arquivo_personagens)
    entrada_quadros = ler_arquivo(nome_arquivo_quadros)
    log("Entradas lidas")

    personagens = processar_personagens(entrada_personagens)
    quadros = processar_quadros(entrada_quadros, personagens)
    saida = gerar_saida(quadros)
    with open("saida.txt", "w") as arquivo_saida:
        arquivo_saida.write(saida)

nome_arquivo_personagens = 'personagens.txt'
nome_arquivo_quadros = 'quadros.txt'

log("Lendo entradadas")

entrada_personagens = ler_arquivo(nome_arquivo_personagens)
entrada_quadros = ler_arquivo(nome_arquivo_quadros)

log("Entradas lidas")

personagens = processar_personagens(entrada_personagens)
quadros = processar_quadros(entrada_quadros, personagens)
saida = gerar_saida(quadros)
with open("saida.txt", "w") as arquivo_saida:
   arquivo_saida.write(saida)
