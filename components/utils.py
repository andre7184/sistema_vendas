import inspect

def obter_colunas(classe):
    # Obtém a lista de parâmetros do construtor da classe
    params = inspect.signature(classe.__init__).parameters
    # Cria uma lista de valores padrão para os parâmetros
    args = [0 if param.default is inspect.Parameter.empty else param.default for param in params.values() if param.name != 'self']
    # Cria uma instância da classe com os valores padrão
    instancia = classe(*args)
    return list(instancia.__dict__.keys())