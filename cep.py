from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def consultar_cep(cep: str):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'erro' in data:
            return None
        return data
    except requests.RequestException:
        return None

@app.route('/api/consultar-cep', methods=['POST'])
def api_consultar_cep():
    cep = request.json.get('cep', '').strip()
    if not cep or len(cep) != 8 or not cep.isdigit():
        return jsonify({'erro': 'CEP inválido'}), 400

    endereco = consultar_cep(cep)
    if not endereco:
        return jsonify({'erro': 'Endereço não encontrado'}), 404

    return jsonify(endereco)

if __name__ == "__main__":
    app.run(debug=True)
