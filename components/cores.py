# cores.py

# Configurações de cores padrão
CORES_PADRAO = {
    "titulo": "blue",
    "texto": "black",
    "erro": "red",
    "sucesso": "green",
    "fundo": ""
}

# Configurações de cores específicas para componentes
CORES_COMPONENTES = {
    "MainApp": {
        "fundo": "#ADD8E6" # o nome da cor azul claro #ADD8E6
    },
    "Login": {
        "fundo": "#f0f0f0"
    },
    # Adicione outras configurações específicas conforme necessário
}

def obter_cor(componente, tipo):
    """
    Retorna a cor para um tipo específico de um componente.
    Se a cor específica não estiver definida, retorna None.
    """
    return CORES_COMPONENTES.get(componente, {}).get(tipo, CORES_PADRAO.get(tipo, None))