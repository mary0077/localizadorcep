from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Configurando o log para registrar erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache para armazenar resultados recentes
cache = {}

def consultar_cep(cep: str):
    """Consulta o CEP na API ViaCEP e usa cache para evitar requisições repetitivas."""
    if cep in cache:
        return cache[cep]
    
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'erro' in data:
            return None
        
        # Armazena no cache por 10 minutos (simulação, pode usar Redis para mais eficiência)
        cache[cep] = data
        return data
    except requests.RequestException as e:
        logging.error(f"Erro ao consultar API ViaCEP: {e}")
        return None

@app.route('/api/consultar-cep', methods=['POST'])
def api_consultar_cep():
    """Endpoint para consultar CEP"""
    cep = request.json.get('cep', '').strip()

    # Validação do CEP
    if not cep or len(cep) != 8 or not cep.isdigit():
        return jsonify({'erro': 'Formato de CEP inválido. Digite um CEP com 8 números.'}), 400

    endereco = consultar_cep(cep)
    if not endereco:
        return jsonify({'erro': 'CEP não encontrado.'}), 404

    return jsonify(endereco)

if __name__ == "__main__":
    app.run(debug=True, port=8013)
