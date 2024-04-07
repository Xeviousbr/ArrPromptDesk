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

def processar_estilo(linha):
    if 'no estilo' in linha:
        return linha.split('no estilo')[1].strip()
    return None

def processar_descricao(linhas, index_personagens):
    # A descrição começa na linha seguinte à linha "Personagens:"
    if index_personagens < len(linhas) - 1:
        descricao = linhas[index_personagens + 1].strip()
        # Remover aspas no início e no final, se houver
        if descricao.startswith('"') and descricao.endswith('"'):
            descricao = descricao[1:-1].strip()
        return descricao
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
        if i < len(quadros) - 1:  
            saida += "\n" + "-" * 16 + "\n"  
    return saida.rstrip()  

def log(mensagem):
    global primeira_chamada_log
    modo = 'w' if primeira_chamada_log else 'a'
    with open("log.txt", modo) as arquivo_log:
        arquivo_log.write(mensagem + "\n")
    primeira_chamada_log = False

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='ISO-8859-1') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return ""

def processar_quadros(entrada_quadros, personagens):
    log("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        log("Nenhum quadro encontrado no arquivo.")
        return quadros
    quadros_texto = entrada_quadros.split("Desenhe o ")[1:]
    log(f"Total de quadros identificados: {len(quadros_texto)}")
    for i, quadro_texto in enumerate(quadros_texto, start=1):  # Começa a contar do 1
        linhas = quadro_texto.strip().split('\n')
        estilo, personagens_quadro, descricao = None, [], None
        for linha in linhas:
            log(f"Linha processada: {linha}")
            if not estilo:
                estilo = processar_estilo(linha)
                log(f"Estilo processado: {estilo}")
            elif 'Personagens:' in linha:
                personagens_quadro = extrair_personagens_do_quadro(linha, personagens)
                log(f"Personagens processados: {', '.join([p.nome for p in personagens_quadro])}")
            elif descricao is None:
                descricao = linha.strip('"')
                log(f"Descrição processada: {descricao}")
        if estilo and descricao:
            quadro = criar_quadro(estilo, descricao, personagens_quadro, i)  # Passa o número do quadro
            quadros.append(quadro)
            log(f"Quadro processado com sucesso.")
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {[p.nome for p in personagens_quadro]}, Descrição: {descricao}")
    return quadros

def processar_dados():
    log("Lendo entradas")
    nome_arquivo_personagens = 'personagens.txt'
    nome_arquivo_quadros = 'quadros.txt'    
    entrada_personagens = ler_arquivo(nome_arquivo_personagens)
    entrada_quadros = ler_arquivo(nome_arquivo_quadros)
    log("Entradas lidas")
    personagens = processar_personagens(entrada_personagens)
    quadros = processar_quadros(entrada_quadros, personagens)
    saida = gerar_saida(quadros)
    with open("saida.txt", "w", encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(saida)

def extrair_personagens_do_quadro(linha, personagens_dict):
    personagens_quadro = []
    if 'Personagens:' in linha:
        nomes_personagens = [nome.strip().rstrip('.') for nome in linha.split(':')[1].split(',')]
        for nome in nomes_personagens:
            if nome in personagens_dict:
                personagens_quadro.append(personagens_dict[nome])
            else:
                log(f"Personagem '{nome}' não encontrado.")
    return personagens_quadro

def criar_quadro(estilo, descricao, personagens_quadro, numero_quadro):
    descricao_completa = f"Desenhe o Quadro no estilo {estilo}.\n{descricao}\n"
    for p in personagens_quadro:
        descricao_completa += f"{p.nome}: {p.descricao}\n"
    descricao_completa = descricao_completa.strip() + str(numero_quadro)  
    return Quadro(estilo, descricao, personagens_quadro, descricao_completa)