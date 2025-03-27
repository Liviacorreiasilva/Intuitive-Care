# 1 - IMPORTAÇÃO DAS BIBLIOTECAS:
import requests  #envia a requisições HTTP
from bs4 import BeautifulSoup  #analisa o documento HTML para extrair os dados
import zipfile   #cria os arquivos zip com o arquivo em pdf
import pathlib  #manipulacao de arquivos e caminho dos arquivos
import os  #acessar os caminhos de arquivos e diretórios 
import PyPDF2  #faz a leitura dos PDFs e extair os textos de arquivos pdf
import csv  #salva os os dados do pdf em CSV

#url do site e url do anexos I e anexo 2 em PDF:
url_site = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
url_anexo1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
url_anexo2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

# 2- FUNCAO PARA ACESSAR A PAGINA WEB E EXTRAIR OS LINKS DO PDF:
def get_pdf_links(url):
    response = requests.get(url)  #Envia a requisição GET para a URL
    soup = BeautifulSoup(response.content, 'html.parser') #Converte o conteúdo HTML em um objeto BeautifulSoup
    return [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')] #Retorna todos os links com extensão .pdf

# 3-  FUNÇAO PARA BAIXAR OS ARQUIVOS PDF:
def download_pdfs(pdf_links, download_folder="baixados_pdfs"): 
    pathlib.Path(download_folder).mkdir(parents=True, exist_ok=True) #Verifica se a pasta de download existe,caso  nao existir sera criada uma pasta usando makedirs
    pdf_paths = [] #criacao de uma lita  para armazenar os caminhos dos arquivos do pdf baixado.
    for pdf_url in pdf_links:  #Percorre todos os links de PDF
        full_url = pdf_url if pdf_url.startswith("http") else "https://www.gov.br" + pdf_url #Corrige link relativo
        pdf_name = os.path.basename(full_url) #Extrai o nome do arquivo PDF a partir do link
        pdf_path = pathlib.Path(download_folder) / pdf_name ##Cria o caminho completo do arquivo pdf salvo 
        with open(pdf_path, 'wb') as f: #Abre o arquivo em modo binário para escrita
            f.write(requests.get(full_url).content) # Baixa o conteúdo do PDF e escreve no arquivo
        pdf_paths.append(pdf_path)  #Adiciona o caminho do PDF à lista
    return pdf_paths #Retorna a lista com os caminhos dos arquivos PDF baixados

# 4- FUNCAO PARA COMPACTAR OS ARQUIVOS PDF EM UM UNICO ARQUIVO ZIP:
def compactar_pdfs(pdf_paths, zip_filename="rol_procedimentos.zip"):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:  #cria um novo arquivo zip
        for pdf in pdf_paths: #Percorre todos os arquivos PDF
            zipf.write(pdf, arcname=pdf.name)  #Adiciona o PDF ao ZIP, sem o caminho completo

# 5 - FUNCAO PARA EXTRAIR O TEXTO DO PDF:
def extrair_pdf_data(pdf_path):
    with open(pdf_path, "rb") as file: #Abre o arquivo PDF em modo de leitura binária
        reader = PyPDF2.PdfReader(file) #Cria o leitor de PDF
        return "\n".join(page.extract_text() for page in reader.pages)  #Extrai o texto de todas as páginas

#7 - FUNCAO PARA SALVAR OS DADOS ESTRAIDOS EM CSV: 
def salvar_dados_csv(data, csv_filename="rol_procedimentos.csv"):
    rows = [line.split("\t") for line in data.split("\n")] #Divide o texto extraído em linhas e colunas
    with open(csv_filename, 'w', newline='') as csvfile: #Abre o arquivo CSV em modo escrita
        csv.writer(csvfile).writerows(rows)  #Escreve as linhas no arquivo CSV

#8 - FUCAO PARA COMPACTAR O ARQUIVO CSV EM ARQUIVO ZIP: 
def compactar_csv(csv_filename, zip_filename="Teste_Livia_Correia_da_Silva.zip"):
    with zipfile.ZipFile(zip_filename, 'w') as zipf: #Cria o arquivo ZIP
        zipf.write(csv_filename) #Adiciona o arquivo CSV ao ZIP

#9 - FUNCAO PRINCIPAL
def main():
    #Obtem os links dos PDFs
    pdf_links = get_pdf_links(url_site)

    #Baixar os PDFs a partir do link
    pdf_paths = download_pdfs(pdf_links)

    #Compacta os PDFs em um arquivo ZIP
    compress_pdfs(pdf_paths)

    #Extrai os  dados do primeiro PDF Anexo I
    pdf_data = extract_pdf_data(pdf_paths[0])

    #Salva os dados extraídos em CSV
    save_data_to_csv(pdf_data)

    #Compacta o arquivo CSV em um arquivo ZIP
    compress_csv("rol_procedimentos.csv")

    #imprime a mensagem no final
    print("Processo completo!")

# Executar o script
if __name__ == "__main__": #Verifica se o script está sendo executado diretamente e, em caso afirmativo, chama a função main() para rodar o processo.


    main()
