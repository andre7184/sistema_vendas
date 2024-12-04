from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import bcrypt
from db.crud import CRUD

app = Flask(__name__)
api = Api(app)

crud = CRUD()


class HealthCheck(Resource):
    def get(self):
        return {'status': 'ok'}, 200

class Cliente(Resource):
    def get(self, id=None):
        if id:
            try:
                cliente = crud.buscar_por_id('clientes', ['id', 'nome', 'cpf', 'endereco'], 'id', id)
                if cliente:
                    # Convertendo a lista para um dicionário
                    cliente_dict = {
                        'id': cliente[0],
                        'nome': cliente[1],
                        'cpf': cliente[2],
                        'endereco': cliente[3]
                    }
                    return jsonify(cliente_dict)
                return {'message': 'Cliente não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            nome = request.args.get('nome')
            if nome:
                try:
                    clientes = crud.buscar_por_nome('clientes', ['id', 'nome', 'cpf', 'endereco'], 'nome', nome)
                    # Convertendo cada cliente para um dicionário
                    clientes_dict = [
                        {'id': cliente[0], 'nome': cliente[1], 'cpf': cliente[2], 'endereco': cliente[3]}
                        for cliente in clientes
                    ]
                    return jsonify(clientes_dict)
                except Exception as e:
                    return {'message': str(e)}, 500
            else:
                try:
                    clientes = crud.listar('clientes', ['id', 'nome', 'cpf', 'endereco'])
                    # Convertendo cada cliente para um dicionário
                    clientes_dict = [
                        {'id': cliente[0], 'nome': cliente[1], 'cpf': cliente[2], 'endereco': cliente[3]}
                        for cliente in clientes
                    ]
                    return jsonify(clientes_dict)
                except Exception as e:
                    return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        print(data)
        try:
            cliente_id = crud.criar('clientes', ['nome', 'cpf', 'endereco'], [data['nome'], data['cpf'], data['endereco']])
            return {'id': cliente_id, 'message': 'Cliente criado com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    def put(self, id):
        data = request.get_json()
        try:
            crud.atualizar('clientes', ['nome', 'cpf', 'endereco'], [data['nome'], data['cpf'], data['endereco']], 'id', id)
            return {'message': 'Cliente atualizado com sucesso'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class Produto(Resource):
    def get(self, id=None):
        if id:
            try:
                produto = crud.buscar_por_id('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'], 'id', id)
                if produto:
                    # Convertendo a lista para um dicionário
                    produto_dict = {
                        'id': produto[0],
                        'nome': produto[1],
                        'descricao': produto[2],
                        'quantidade': produto[3],
                        'valor': produto[4]
                    }
                    return jsonify(produto_dict)
                return {'message': 'Produto não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            nome = request.args.get('nome')
            if nome:
                try:
                    produtos = crud.buscar_por_nome('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'], 'nome', nome)
                    # Convertendo cada produto para um dicionário
                    produtos_dict = [
                        {'id': produto[0], 'nome': produto[1], 'descricao': produto[2], 'quantidade': produto[3], 'valor': produto[4]}
                        for produto in produtos
                    ]
                    return jsonify(produtos_dict)
                except Exception as e:
                    return {'message': str(e)}, 500
            else:
                try:
                    produtos = crud.listar('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'])
                    # Convertendo cada produto para um dicionário
                    produtos_dict = [
                        {'id': produto[0], 'nome': produto[1], 'descricao': produto[2], 'quantidade': produto[3], 'valor': produto[4]}
                        for produto in produtos
                    ]
                    return jsonify(produtos_dict)
                except Exception as e:
                    return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        try:
            crud.criar('produtos', ['nome', 'descricao', 'quantidade', 'valor'], [data['nome'], data['descricao'], data['quantidade'], data['valor']])
            return {'message': 'Produto criado com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    def put(self, id):
        data = request.get_json()
        try:
            crud.atualizar('produtos', ['nome', 'descricao', 'quantidade', 'valor'], [data['nome'], data['descricao'], data['quantidade'], data['valor']], 'id', id)
            return {'message': 'Produto atualizado com sucesso'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class Venda(Resource):
    def get(self, id=None):
        if id:
            try:
                venda = crud.buscar_por_id('vendas', ['id', 'cliente_id', 'vendedor_id', 'data_venda', 'forma_pagamento', 'quantidade_parcelas'], 'id', id)
                if venda:
                    itens = crud.buscar_por_condicao('itens_venda', ['id', 'venda_id', 'produto_id', 'quantidade', 'valor_unitario'], 'venda_id = %s', (id,))
                    venda['itens'] = itens
                    return jsonify(venda)
                return {'message': 'Venda não encontrada'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            data_venda = request.args.get('data_venda')
            if data_venda:
                try:
                    vendas = crud.buscar_por_data('vendas', ['id', 'cliente_id', 'vendedor_id', 'data_venda', 'forma_pagamento', 'quantidade_parcelas'], 'data_venda', data_venda)
                    return jsonify(vendas)
                except Exception as e:
                    return {'message': str(e)}, 500
            else:
                try:
                    vendas = crud.listar('vendas', ['id', 'cliente_id', 'vendedor_id', 'data_venda', 'forma_pagamento', 'quantidade_parcelas'])
                    return jsonify(vendas)
                except Exception as e:
                    return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        try:
            crud.criar('vendas', ['cliente_id', 'vendedor_id', 'data_venda', 'forma_pagamento', 'quantidade_parcelas'],
                       [data['cliente_id'], data['vendedor_id'], data['data_venda'], data['forma_pagamento'], data['quantidade_parcelas']])
            venda_id = crud.db_manager.cursor.lastrowid
            for item in data['itens']:
                crud.criar('itens_venda', ['venda_id', 'produto_id', 'quantidade', 'valor_unitario'],
                           [venda_id, item['produto_id'], item['quantidade'], item['valor_unitario']])
            return {'message': 'Venda criada com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

class Usuario(Resource):
    def get(self, id=None):
        if id:
            try:
                usuario = crud.buscar_por_id('usuarios', ['id', 'nome', 'login', 'senha', 'tipo'], 'id', id)
                if usuario:
                    # Convertendo a lista para um dicionário
                    usuario_dict = {
                        'id': usuario[0],
                        'nome': usuario[1],
                        'login': usuario[2],
                        'senha': usuario[3],
                        'tipo': usuario[4]
                    }
                    return jsonify(usuario_dict)
                return {'message': 'Usuário não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            try:
                usuarios = crud.listar('usuarios', ['id', 'nome', 'login', 'senha', 'tipo'])
                # Convertendo cada usuário para um dicionário
                usuarios_dict = [
                    {'id': usuario[0], 'nome': usuario[1], 'login': usuario[2], 'senha': usuario[3], 'tipo': usuario[4]}
                    for usuario in usuarios
                ]
                return jsonify(usuarios_dict)
            except Exception as e:
                return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        senha_hashed = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            crud.criar('usuarios', ['nome', 'login', 'senha', 'tipo'], [data['nome'], data['login'], senha_hashed, data['tipo']])
            return {'message': 'Usuário criado com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    def put(self, id):
        data = request.get_json()
        senha_hashed = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            crud.atualizar('usuarios', ['nome', 'login', 'senha', 'tipo'], [data['nome'], data['login'], senha_hashed, data['tipo']], 'id', id)
            return {'message': 'Usuário atualizado com sucesso'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class Autenticacao(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')
        senha = data.get('senha')
        
        try:
            print(f"Tentando autenticar usuário: {login}")
            usuario = crud.buscar_por_condicao('usuarios', ['id', 'nome', 'login', 'senha', 'tipo'], 'login = %s', (login,))
            print(f"Usuário encontrado: {usuario}")
            if usuario:
                usuario_dict = {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'login': usuario[2],
                    'senha': usuario[3],
                    'tipo': usuario[4]
                }
                print(f"Usuário convertido em dicionário: {usuario_dict}")
                if bcrypt.checkpw(senha.encode('utf-8'), usuario_dict['senha'].encode('utf-8')):
                    print("Senha correta")
                    return jsonify({
                        'id': usuario_dict['id'],
                        'nome': usuario_dict['nome'],
                        'login': usuario_dict['login'],
                        'tipo': usuario_dict['tipo']
                    })
                else:
                    print("Senha incorreta")
                    return {'message': 'Credenciais inválidas'}, 401
            else:
                print("Usuário não encontrado")
                return {'message': 'Credenciais inválidas'}, 401
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return {'message': str(e)}, 500

api.add_resource(HealthCheck, '/health')
api.add_resource(Cliente, '/clientes', '/clientes/<int:id>')
api.add_resource(Produto, '/produtos', '/produtos/<int:id>')
api.add_resource(Venda, '/vendas', '/vendas/<int:id>')
api.add_resource(Usuario, '/usuarios', '/usuarios/<int:id>')
api.add_resource(Autenticacao, '/usuarios/autenticar')

if __name__ == '__main__':
    app.run(debug=True)