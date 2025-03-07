from flask import Flask, request, jsonify, render_template
from db import db, Creditos
from logging import exception
import os

template_dir = os.path.dirname(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir, static_url_path="/static")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "database", "creditos.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#Rutas de la aplicación
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/creditlist', methods=['GET'])
def frontlistcredit():
    return render_template('creditlist.html')

@app.route('/api/addcredit', methods=['POST'])
def addcredit():
    try:
        print(request.form)

        cliente = request.form["name"]
        monto = request.form["amount"]
        tasa_interes = request.form["interest_rate"]
        plazo = request.form["term"]
        fecha_otorgamiento = request.form["date_of_grant"]

        newcredit = Creditos(cliente, float(monto), float(tasa_interes), int(plazo), fecha_otorgamiento)
        db.session.add(newcredit)
        db.session.commit()

        return jsonify(newcredit.serialize()), 200
    
    except Exception:
        exception("\n[SERVER]: Error in route /api/addcredit. Log: \n")
        return jsonify({"msg": "Algo ha salido mal, al agregar un nuevo credito"}), 500

@app.route('/api/creditlist', methods=['GET'])
def creditlist():
    try:
        creditlist = Creditos.query.all()
        return jsonify([credit.serialize() for credit in creditlist]), 200
    except Exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo ha salido mal"}), 500

@app.route ('/api/editcredit/<int:id>', methods=['PUT'])
def editcredit(id):
    try:
        creditedit = db.session.get(Creditos, id)
        if not creditedit:
            return jsonify({"msg": "Registro no encontrado"}), 404
        
        creditedit.cliente = request.json["cliente"]
        creditedit.monto = request.json["monto"]
        creditedit.tasa_interes = request.json["tasa_interes"]
        creditedit.plazo = request.json["plazo"]
        creditedit.fecha_otorgamiento = request.json["fecha_otorgamiento"]
        

        db.session.commit()

        return jsonify(creditedit.serialize(), 200)

    except Exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo salio mal con la peticion de edición de registro"}), 500 

@app.route ('/api/deletecredit/<int:id>', methods=['DELETE'])
def deletecredit(id):
    try:
        creditdelete = Creditos.query.get(id)
        if not creditdelete:
            return jsonify({"msg": "Registro no encontrado"}), 404
        
        db.session.delete(creditdelete)
        db.session.commit()

        return jsonify({"msg":"Credito eliminado con éxito"}), 200
    
    except Exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo salió mal al eliminar el registro"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3030)