from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sqlite3
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do Banco de Dados
def init_db():
    with sqlite3.connect("ceps.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico (id INTEGER PRIMARY KEY, cep TEXT, endereco TEXT)''')
        conn.commit()

init_db()

def salvar_no_banco(cep, endereco):
    with sqlite3.connect("ceps.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historico (cep, endereco) VALUES (?, ?)", (cep, endereco))
        conn.commit()

def consultar_cep(cep: str):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if 'erro' in data:
            return None
        endereco = f"{data['logradouro']}, {data['bairro']}, {data['localidade']} - {data['uf']}"
        salvar_no_banco(cep, endereco)
        return data
    except requests.RequestException as e:
        logging.error(f"Erro ao consultar API ViaCEP: {e}")
        return None

@app.route('/api/consultar-cep', methods=['POST'])
def api_consultar_cep():
    cep = request.json.get('cep', '').strip()
    if not cep or len(cep) != 8 or not cep.isdigit():
        return jsonify({'erro': 'Formato de CEP inválido. Digite um CEP com 8 números.'}), 400
    endereco = consultar_cep(cep)
    if not endereco:
        return jsonify({'erro': 'CEP não encontrado.'}), 404
    return jsonify(endereco)

if __name__ == "__main__":
    app.run(debug=True, port=8013)
