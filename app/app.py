# ./app/app.py
from flask import Flask, Response, render_template, request, jsonify
from bson.json_util import dumps
from pymongo import MongoClient
from bson import ObjectId
from flask_restful import Resource, Api, abort, reqparse

import os

PEOPLE_FOLDER = os.path.join('static', 'pato')

app = Flask(__name__, static_folder='/app/static',
            template_folder='/app/templates')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

api = Api(app)

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017)

# Base de datos
db = client.cockteles


#######################################################################


@app.route('/')
def index():
    return render_template("index.html")


#######################################################################


@app.route('/imagen')
def imagen():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pato.jpg')
    return render_template("imagen.html", user_image=full_filename)


#######################################################################


@app.route('/fibonacci/<int:lectura>')
def fibonacci(lectura):

    # var iniciales
    n1, n2 = 0, 1
    contador = 2
    aux = 0

    # check lectura positiva
    if lectura <= 0:
        return "Lectura erronea: Valor negativo"

    # check lectura = 1
    elif lectura == 1:
        return "Numero leido: 1 Numero obtenido: 0"

    # check lectura = 2
    elif lectura == 2:
        return "Numero leido: 2 Numero obtenido: 1"

    # hacer Fibonacci
    else:
        while contador < lectura:
            aux = n1 + n2
            # update values
            n1 = n2
            n2 = aux
            contador += 1

    resultado = "Numero leido: "
    resultado += str(lectura)
    resultado += " Numero obtenido: "
    resultado += str(aux)
    return resultado


#######################################################################


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


#######################################################################


@app.route('/todas_las_recetas')
def mongo():
    # Encontramos los documentos de la coleccion "recipes"
    recetas = db.recipes.find()  # devuelve un cursor(*), no una lista ni un iterador

    lista_recetas = []
    for receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
    return Response(resJson, mimetype='application/json')


#######################################################################


@app.route('/recetas_con/<string:ingrediente>')
def busca_ingrediente(ingrediente):
    # Encontramos los documentos de la coleccion "recipes"
    # devuelve un cursor(*), no una lista ni un iterador
    recetas = db.recipes.find({"ingredients.name": ingrediente})

    lista_recetas = []
    for receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
    return Response(resJson, mimetype='application/json')


#######################################################################


@app.route('/recetas_compuestas_de/<int:numero>/ingredientes')
def busca_num_ingrediente(numero):
    # Encontramos los documentos de la coleccion "recipes"
    # devuelve un cursor(*), no una lista ni un iterador
    recetas = db.recipes.find({"ingredients": {"$size": 2}})

    lista_recetas = []
    for receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
    return Response(resJson, mimetype='application/json')

################################################################################
# FLASK REST API
################################################################################

def abort_if_dont_exist(un_id):
    buscado = db.recipes.find_one({'_id': ObjectId(un_id)})
    if buscado:
        pass
    else:
        abort(404, message="Receta no existente".format(un_id))

parser = reqparse.RequestParser()
parser.add_argument('_id')
parser.add_argument('name')
parser.add_argument('garnish')
parser.add_argument('instructions')
parser.add_argument('ingredients', type=dict)

class Receta(Resource):
    def get(self, un_id):
        abort_if_dont_exist(un_id)
        buscado = db.recipes.find_one({'_id': ObjectId(un_id)})
        # casting a string (es un ObjectId)
        buscado['_id'] = str(buscado['_id'])
        return jsonify(buscado)

    def delete(self, un_id):
        abort_if_dont_exist(un_id)
        db.recipes.delete_one(db.recipes.find_one({'_id': ObjectId(un_id)}))
        return '', 204

    def put(self, un_id):
        abort_if_dont_exist(un_id)
        args = parser.parse_args()
        receta = {
            "_id": args['_id'],
            "name": args['name'],
            "instructions": args['instructions'],
            "ingredients": args['ingredients'],
            "garnish": args['garnish']
        }

        buscado = db.recipes.find_one({'_id': ObjectId(un_id)})

        if (args['_id']==None):
            receta["_id"] = buscado['_id']
            
        if (args['name']==None):
            receta["name"] = buscado['name']
            receta["slug"] = receta["name"].lower().replace(" ", "-")
        if (args['instructions']==None):
            receta["instructions"] = buscado['instructions']
        if (args['ingredients']==None):
            receta["ingredients"] = buscado['ingredients']
        if (args['garnish']==None):
            receta["garnish"] = buscado['garnish']
        receta["slug"] = receta["name"].lower().replace(" ", "-")
        
        db.recipes.delete_one(buscado)
        db.recipes.insert_one(receta)
        receta['_id'] = str(receta['_id'])
        return receta, 201

class Recetas(Resource):
    def get(self):
        lista = []
        buscados = db.recipes.find().sort('name')
        for recipe in buscados:
            # casting a string (es un ObjectId)
            recipe['_id'] = str(recipe['_id'])
            lista.append(recipe)
        return jsonify(lista)
    
    def post(self):
        args = parser.parse_args()
        receta = {
            "_id": args['_id'],
            "name": args['name'],
            "garnish": args['garnish'],
            "slug": ""
        } 
        receta["slug"] = receta["name"].lower().replace(" ", "-")       
        db.recipes.insert_one(receta)
        return receta, 201

api.add_resource(Recetas, '/api/recipes')
api.add_resource(Receta, '/api/recipes/<un_id>')

if __name__ == "__main__":
    app.run(debug=True)

""" #######################################################################
@app.route('/postrecipes')
def postrecipes():
    return render_template('PostRecipes.html')


@app.route('/api/recipes', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        lista = []
        buscados = db.recipes.find().sort('name')
        for recipe in buscados:
            # casting a string (es un ObjectId)
            recipe['_id'] = str(recipe['_id'])
            lista.append(recipe)
        return jsonify(lista)

    if request.method == 'POST':
        receta = {
            "_id": request.form['_id'],
            "name": request.form['nombre'],
            "ingredients": [],
            "instructions": [],
            "garnish": request.form['guarnicion'],
            "slug": request.form['nombre'].lower().replace(" ", "-")
        }
        if (request.form['paso1'] != ""):
            receta["instructions"].append(request.form['paso1'])
        if (request.form['paso2'] != ""):
            receta["instructions"].append(request.form['paso2'])
        if (request.form['paso3'] != ""):
            receta["instructions"].append(request.form['paso3'])
        if (request.form['paso4'] != ""):
            receta["instructions"].append(request.form['paso4'])

        for i in range (1,5) :
            
            ingr = {
                "name": request.form[f'nom_ing{i}'],
                "quantity": {
                    "value": request.form[f'cant_ing{i}'],
                    "unit": request.form[f'med_ing{i}']
                }
            }
            if (request.form[f'nom_ing{i}'] != "") and (request.form[f'cant_ing{i}'] != "") and (request.form[f'med_ing{i}'] != ""):
                receta["ingredients"].append(ingr)

        
        db.recipes.insert_one(receta)
        return jsonify(receta)


@app.route('/api/recipes/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_2(id):
    if request.method == 'GET':
        buscado = db.recipes.find_one({'_id': ObjectId(id)})
        if buscado:
            # casting a string (es un ObjectId)
            buscado['_id'] = str(buscado['_id'])
            return jsonify(buscado)
        else:
            return jsonify({'error': 'Not found'}), 404

    if request.method == 'PUT':
        buscado = db.recipes.find_one({'_id': ObjectId(id)})
        
        if buscado:
            db.recipes.update_one(buscado,{ '$set' : {'garnish':'patatas'}})
            buscado = db.recipes.find_one({'_id': ObjectId(id)})
            resJson = dumps(buscado)
            return Response(resJson, mimetype='application/json')
        else:
            return jsonify({'error': 'Not found'}), 404

    if request.method == 'DELETE':
        buscado = db.recipes.find_one({'_id': ObjectId(id)})
        if buscado:
            db.recipes.delete_one(buscado)
            return id
        else:
            return jsonify({'error': 'Not found'}), 404 """