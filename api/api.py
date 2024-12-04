from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from mysql.connector import Error
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
                    return jsonify(cliente)
                return {'message': 'Cliente não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            nome = request.args.get('nome')
            if nome:
                try:
                    clientes = crud.buscar_por_nome('clientes', ['id', 'nome', 'cpf', 'endereco'], 'nome', nome)
                    return jsonify(clientes)
                except Exception as e:
                    return {'message': str(e)}, 500
            else:
                try:
                    clientes = crud.listar('clientes', ['id', 'nome', 'cpf', 'endereco'])
                    return jsonify(clientes)
                except Exception as e:
                    return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        try:
            crud.criar('clientes', ['nome', 'cpf', 'endereco'], [data['nome'], data['cpf'], data['endereco']])
            return {'message': 'Cliente criado com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

class Produto(Resource):
    def get(self, id=None):
        if id:
            try:
                produto = crud.buscar_por_id('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'], 'id', id)
                if produto:
                    return jsonify(produto)
                return {'message': 'Produto não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            nome = request.args.get('nome')
            if nome:
                try:
                    produtos = crud.buscar_por_nome('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'], 'nome', nome)
                    return jsonify(produtos)
                except Exception as e:
                    return {'message': str(e)}, 500
            else:
                try:
                    produtos = crud.listar('produtos', ['id', 'nome', 'descricao', 'quantidade', 'valor'])
                    return jsonify(produtos)
                except Exception as e:
                    return {'message': str(e)}, 500

    def post(self):
        data = request.get_json()
        try:
            crud.criar('produtos', ['nome', 'descricao', 'quantidade', 'valor'], [data['nome'], data['descricao'], data['quantidade'], data['valor']])
            return {'message': 'Produto criado com sucesso'}, 201
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
                    return jsonify(usuario)
                return {'message': 'Usuário não encontrado'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            try:
                usuarios = crud.listar('usuarios', ['id', 'nome', 'login', 'senha', 'tipo'])
                return jsonify(usuarios)
            except Exception as e:
                return {'message': str(e)}, 500

api.add_resource(HealthCheck, '/health')
api.add_resource(Cliente, '/clientes', '/clientes/<int:id>')
api.add_resource(Produto, '/produtos', '/produtos/<int:id>')
api.add_resource(Venda, '/vendas', '/vendas/<int:id>')
api.add_resource(Usuario, '/usuarios', '/usuarios/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)