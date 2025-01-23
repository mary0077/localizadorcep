import requests
from typing import Optional


def validar_cep(cep: str) -> Optional[str]:
    """
    Valida e limpa o CEP, removendo caracteres não numéricos e verificando se tem 8 dígitos.

    Args:
        cep (str): O CEP informado pelo usuário.

    Returns:
        Optional[str]: O CEP validado e limpo, ou None se inválido.
    """
    cep = ''.join(filter(str.isdigit, cep))
    return cep if len(cep) == 8 else None


def consultar_cep(cep: str) -> Optional[dict]:
    """
    Consulta informações de um CEP usando a API ViaCEP.

    Args:
        cep (str): O CEP a ser consultado.

    Returns:
        Optional[dict]: Os dados do endereço se encontrado, ou None se não encontrado ou erro.
    """
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Levanta exceções para status HTTP 4xx e 5xx
        data = response.json()

        if 'erro' in data:
            return None  # CEP não encontrado
        return data
    except requests.RequestException as e:
        print(f"Erro ao consultar o CEP: {e}")
        return None


def exibir_endereco(data: dict) -> None:
    """
    Exibe as informações do endereço de forma estruturada.

    Args:
        data (dict): Os dados do endereço retornados pela API.
    """
    print("Endereço encontrado:")
    print(f"Logradouro: {data.get('logradouro', 'Não informado')}")
    print(f"Bairro: {data.get('bairro', 'Não informado')}")
    print(f"Cidade: {data.get('localidade', 'Não informado')}")
    print(f"Estado: {data.get('uf', 'Não informado')}")


def localizar_cep(cep: str) -> None:
    """
    Localiza e exibe informações de um CEP informado.

    Args:
        cep (str): O CEP a ser localizado.
    """
    cep_validado = validar_cep(cep)
    if not cep_validado:
        print("CEP inválido. Certifique-se de que o CEP tenha 8 dígitos.")
        return

    endereco = consultar_cep(cep_validado)
    if endereco:
        exibir_endereco(endereco)
    else:
        print(f"Não foi possível localizar informações para o CEP {cep_validado}.")


if __name__ == "__main__":
    # Solicita o CEP ao usuário
    cep_input = input("Digite o CEP (apenas números): ").strip()
    localizar_cep(cep_input)
