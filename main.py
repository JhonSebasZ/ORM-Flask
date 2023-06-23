from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #orm
from flask_marshmallow import Marshmallow

app = Flask(__name__) #nombre de la aplicacion


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/orm_flask'
db = SQLAlchemy(app) #utilizar la app en SQLAlchemy
ma = Marshmallow(app) #utilizaer serializacion en la app

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apellido = db.Column(db.String(45))
    nombre = db.Column(db.String(45))
    email = db.Column(db.String(45))

    def __init__(self,apellido,nombre,email):
        self.apellido = apellido
        self.nombre = nombre
        self.email = email
    
# clase para serializar (convertir a json)
class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('apellido','nombre', 'email')


#objeto para serializar todos los clientes de la tabla y mostrarlos
clientes_schema = ClienteSchema(many=True)

#objeto para serializar solo un cliente
cliente_schema = ClienteSchema()

#endpoint para mostrar a todos los clientes
@app.route('/all_clientes', methods=['GET'])
def all_clientes():
    all_clientes = Clientes.query.all()
    result = clientes_schema.dump(all_clientes)
    return jsonify(result) #retorna objeto convertido a json

#endpoint para mostrar a todos los clientes
@app.route('/cliente/<id>', methods=['GET'])
def find_cliente(id):
    cliente = Clientes.query.get(id)
    return cliente_schema.jsonify(cliente)

#endpoint para crear un clientes
@app.route('/cliente', methods=['POST'])
def create_cliente():
    apellido = request.json['apellido']
    nombre = request.json['nombre']
    email = request.json['email']
    new_cliente = Clientes(apellido, nombre, email)
    db.session.add(new_cliente) #Guarda en la sesion sel cliente
    db.session.commit()
    cliente = Clientes.query.get(new_cliente.id)

    return cliente_schema.jsonify(cliente)

#endpoint para actualizar un clientes
@app.route('/cliente/<id>', methods=['PUT'])
def update_cliente(id):
    cliente = Clientes.query.get(id)

    apellido = request.json['apellido']
    nombre = request.json['nombre']
    email = request.json['email']

    cliente.apellido = apellido
    cliente.nombre = nombre
    cliente.email = email

    db.sesion.commit()
    return cliente_schema.jsonify(cliente)

#endpoint para eliminar un clientes
@app.route('/cliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)



app.run(debug=True) #servidor 
