# importação
from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user


# ORM - Object Relation Mapper (Objeto de Relação Mapeador), gera uma camada de abstração para o Banco de Dados. O código reage com o ORM e o ORM interage com o Banco de Dados.

app = Flask(__name__) #instancia a variável Flask
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"

login_manager = LoginManager()
db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Modelagem 
#User (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)


#Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Rota de Login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    # data.get("username")

    user = User.query.filter_by(username=data.get("username")).first()

    # if user != None:
    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "Logged In Sucessfully"})
    return jsonify({"message": "Unauthorized. Invalid Credentials"}), 401


# Rota de Logout
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout Sucessfully"})

# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/api/products/add', methods=["POST"]) #alt
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description",""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product Added Sucessfully"})
    return jsonify({"message": "Invalid Product Data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    #Recuperar o produto da base de dados
    product = Product.query.get(product_id)
    #Verificar se o produto existe
    if product != None:
    #Se existe, apagar da base de dados
        db.session.delete(product)
        db.session.commit()
    #Se não existe, retornar 404 not found
        return jsonify({"message": "Product Deleted Sucessfully"})
    return jsonify({"message": "Product Not Found"}), 404

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_products_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Product not Found"}), 404


@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not Found"}), 404
    
    data = request.json
    if'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Product Updated Sucessfully'})


@app.route('/api/products', methods=['Get'])
def get_products():
    products = Product.query.all()
    product_list =[]
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        product_list.append(product_data)

    return jsonify(product_list)
        


# Rota raiz (da pag. inicial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True) #ativa o modo depuração e ajuda a receber mais informações quando requisições forem feitas. Não usar quando usar em produção.
