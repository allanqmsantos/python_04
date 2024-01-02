import os
import logging
from datetime import datetime
import shutil 

def ler_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        conteudo = arquivo.read()
    return conteudo

def escrever_arquivo(caminho_arquivo, conteudo):
    with open(caminho_arquivo, "w") as arquivo:
        arquivo.write(conteudo)

def abrir_arquivo(caminho_arquivo):
    os.startfile(caminho_arquivo) # Definir a função abrir_arquivo

def abreviar_arquivo(nome_arquivo):
    # Usar a função split para separar as palavras do nome do arquivo
    palavras = nome_arquivo.split("_")
    # Usar uma compreensão de lista para obter a primeira letra de cada palavra
    letras = [p[0] for p in palavras]
    # Usar a função join para juntar as letras com um "_"
    abreviacao = "_".join(letras)
    # Retornar a abreviacao
    return abreviacao

def versionar_arquivo(caminho_arquivo):
    # Se o arquivo já existir, adicionar um número de versionamento
    if os.path.exists(caminho_arquivo):
        base, extensao = os.path.splitext(caminho_arquivo)
        i = 1
        while os.path.exists(caminho_arquivo):
            caminho_arquivo = f"{base}_v{i}{extensao}"
            i += 1
    return caminho_arquivo

def main():
    # Configurar o logger
    logging.basicConfig(filename=r'\\192.168.254.5\enfermagem\logs\log.txt', level=logging.INFO)

    # Obter informações do funcionário
    nome_funcionario = input("Nome do Funcionário: ").strip().replace(" ", "_")
    cargo = input("Cargo: ").strip().replace(" ", "_")

    # Logar as informações do funcionário
    logging.info(f"Funcionário: {nome_funcionario}, Cargo: {cargo}")

    # Obter informações do paciente
    nome_paciente = input("Digite o nome do paciente: ").strip().replace(" ", "_")
    unidade_internacao = input("Digite a unidade de internação: ").strip().replace(" ", "_")

    # Logar as informações do paciente
    logging.info(f"Paciente: {nome_paciente}, Unidade de Internação: {unidade_internacao}")

    # Nome do arquivo
    nome_arquivo = f"{nome_paciente}_{unidade_internacao}_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}"

    # Caminho do arquivo modelo
    caminho_modelo = fr"\\192.168.254.5\enfermagem"

    # Caminho para salvar os novos arquivos
    caminho_atual = fr"\\192.168.254.5\enfermagem\atuais"

    # Caminho para salvar os backups
    caminho_bkp = fr"\\192.168.254.5\enfermagem\bkp"

    # Lista de arquivos para escolher
    arquivos = [
        "ANOTACAO_DO_TECNICO_MANUAL.docx",
        "EVOLUCAO_TEC_ENFERMAGEM_ENFERMARIA.doc",
        "HBV_SAE.docx",
        "EVOLUCAO_DE_ENFERMEIRO_UTI.pdf"
    ]

    # Menu de escolha
    while True:
        print("Escolha o arquivo a ser aberto:")
        for i, arquivo in enumerate(arquivos, 1):
            print(f"{i}. {arquivo}")
        print("0. Sair")

        opcao = input("Digite o número correspondente ao arquivo desejado: ")

        if opcao == "0":
            print("Saindo do programa...")
            break

        try:
            opcao = int(opcao)
            if opcao < 1 or opcao > len(arquivos):
                raise ValueError
        except ValueError:
            print("Opção inválida. Digite um número correspondente à opção desejada.")
            continue
        

        # Nome do arquivo escolhido
        arquivo_escolhido = arquivos[opcao - 1]

        # Logar o nome do arquivo escolhido
        logging.info(f"Documento: {arquivo_escolhido}")

        # Caminho completo do arquivo escolhido
        caminho_arquivo_escolhido = fr"{caminho_modelo}\{arquivo_escolhido}"

        # Copiar o arquivo modelo para a pasta de arquivos atuais
        shutil.copy(caminho_arquivo_escolhido, caminho_atual) # Usar shutil.copy em vez de os.system

        # Adicionar a extensão ao nome do arquivo
        extensao = os.path.splitext(arquivo_escolhido)[-1] 
        abreviacao = abreviar_arquivo(arquivo_escolhido) 
        novo_caminho = fr"{caminho_atual}\{nome_arquivo}_{abreviacao}{extensao}" # Adicionar a abreviação e a extensão ao nome do arquivo
        novo_caminho = versionar_arquivo(novo_caminho) # Adicionar versionamento ao nome do arquivo
        os.rename(fr"{caminho_atual}\{arquivo_escolhido}", novo_caminho)

        # Logar a data e hora de criação do arquivo
        logging.info(f"Data e Hora de Criação: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        # Copiar o arquivo para a pasta de backup
        shutil.copy(novo_caminho, caminho_bkp)

        # Abrir o arquivo
        abrir_arquivo(novo_caminho)

        # Abrir o Windows Explorer no diretório atual
        os.startfile(caminho_atual)

if __name__ == "__main__":
    main()
