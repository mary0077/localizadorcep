import requests

def localizar_cep(cep):
    # Remover caracteres não numéricos do CEP
    cep = ''.join(filter(str.isdigit, cep))
    
    if len(cep) != 8:
        print("CEP inválido. Certifique-se de que o CEP tenha 8 dígitos.")
        return

    # URL da API ViaCEP
    url = f'https://viacep.com.br/ws/{cep}/json/'

    # Realizando a requisição para a API
    response = requests.get(url)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        if 'erro' in data:
            print(f"O CEP {cep} não foi encontrado.")
        else:
            print(f"Endereço encontrado para o CEP {cep}:")
            print(f"Logradouro: {data['logradouro']}")
            print(f"Bairro: {data['bairro']}")
            print(f"Cidade: {data['localidade']}")
            print(f"Estado: {data['uf']}")
    else:
        print("Erro na requisição. Tente novamente.")

# Solicitando o CEP ao usuário
cep_input = input("Digite o CEP (apenas números): ")
localizar_cep(cep_input)
