# importação
from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy

# ORM - Object Relation Mapper (Objeto de Relação Mapeador), gera uma camada de abstração para o Banco de Dados. O código reage com o ORM e o ORM interage com o Banco de Dados.

app = Flask(__name__) #instancia a variável Flask
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"
db = SQLAlchemy(app)

#Modelagem 
# Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/api/products/add', methods=["POST"]) #alt
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description",""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product Added Sucessfully"})
    return jsonify({"message": "Invalid Product Data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
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



# Rota raiz (da pag. inicial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True) #ativa o modo depuração e ajuda a receber mais informações quando requisições forem feitas. Não usar quando usar em produção.
