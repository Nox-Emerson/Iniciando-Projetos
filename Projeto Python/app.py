# importação
from flask import Flask

app = Flask(__name__) #instancia a variável Flask

# Rota raiz (da pag. inicial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True) #ativa o modo depuração e ajuda a receber mais informações quando requisições forem feitas. Não usar quando usar em produção.
