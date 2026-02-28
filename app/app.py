from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongo', 27017)
db = client.ecommerce_db
products_collection = db.produtos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    """Lista todos os produtos"""
    produtos = list(products_collection.find({}, {'_id': 1, 'nome': 1, 'preco': 1, 'categoria': 1}))
    # Convert ObjectId to string for JSON serialization
    for produto in produtos:
        produto['_id'] = str(produto['_id'])
    return jsonify(produtos)

@app.route('/api/produtos', methods=['POST'])
def create_produto():
    """Cria um novo produto"""
    data = request.get_json()
    
    if not all(k in data for k in ['nome', 'preco', 'categoria']):
        return jsonify({'erro': 'Campos obrigatórios: nome, preco, categoria'}), 400
    
    produto = {
        'nome': data['nome'],
        'preco': float(data['preco']),
        'categoria': data['categoria']
    }
    
    result = products_collection.insert_one(produto)
    return jsonify({'id': str(result.inserted_id), 'mensagem': 'Produto criado com sucesso'}), 201

@app.route('/api/produtos/<id>', methods=['PUT'])
def update_produto(id):
    """Atualiza um produto existente"""
    try:
        produto_id = ObjectId(id)
    except:
        return jsonify({'erro': 'ID inválido'}), 400
    
    data = request.get_json()
    
    if not all(k in data for k in ['nome', 'preco', 'categoria']):
        return jsonify({'erro': 'Campos obrigatórios: nome, preco, categoria'}), 400
    
    atualizado = {
        'nome': data['nome'],
        'preco': float(data['preco']),
        'categoria': data['categoria']
    }
    
    result = products_collection.update_one({'_id': produto_id}, {'$set': atualizado})
    
    if result.matched_count == 0:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    return jsonify({'mensagem': 'Produto atualizado com sucesso'}), 200

@app.route('/produtos')
def produtos():
    """Exibe página com tabela de produtos"""
    produtos_list = list(products_collection.find({}, {'_id': 1, 'nome': 1, 'preco': 1, 'categoria': 1}))
    return render_template('produtos.html', produtos=produtos_list)

@app.route('/produtos/<id>/editar')
def editar_produto(id):
    """Exibe formulário para editar um produto"""
    try:
        produto_id = ObjectId(id)
    except:
        return "ID inválido", 400
    
    produto = products_collection.find_one({'_id': produto_id})
    
    if not produto:
        return "Produto não encontrado", 404
    
    produto['_id'] = str(produto['_id'])
    return render_template('editar_produto.html', produto=produto)

@app.route('/api/produtos/<id>', methods=['DELETE'])
def delete_produto(id):
    """Deleta um produto"""
    try:
        produto_id = ObjectId(id)
    except:
        return jsonify({'erro': 'ID inválido'}), 400
    
    result = products_collection.delete_one({'_id': produto_id})
    
    if result.deleted_count == 0:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200

if __name__ == '__main__':
    # development server; in production we use gunicorn
    app.run(host='0.0.0.0', port=5000)
