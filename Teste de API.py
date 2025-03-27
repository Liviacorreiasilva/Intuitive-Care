from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# Função para carregar dados do CSV
def carregar_dados_csv(caminho_arquivo):
    dados = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
        leitor = csv.DictReader(file)
        for linha in leitor:
            dados.append(linha)
    return dados

# Rota para buscar operadoras por nome
@app.route('/buscar_operadoras', methods=['GET'])
def buscar_operadoras():
    nome_busca = request.args.get('nome')  # Parâmetro 'nome' enviado pela query string
    operadoras = carregar_dados_csv('operadoras_de_plano_de_saude_ativas.csv')  # Carrega os dados do CSV
    resultados = [op for op in operadoras if nome_busca.lower() in op['nome_operadora'].lower()]
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)

