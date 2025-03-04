from flask import Flask, request, jsonify, render_template
from db import db, Credits
from logging import exception
import os

template_dir = os.path.dirname(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database\\credits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/addcredit', methods=['POST'])
def addcredit():
    try:
        cliente = request.form["cliente"]
        monto = request.form["monto"]
        tasa_interes = request.fomr["tasa_interes"]
        plazo = request.form["plazo"]
        fecha_otorgamiento = request.form["fecha_otorgamiento"]

        newcredit = Credits(cliente, float(monto), float(tasa_interes), int(plazo), fecha_otorgamiento)
        db.session.add(newcredit)
        db.session.commit()

        return jsonify(newcredit.serialize()), 200
    
    except Exception:
        Exception("\n[SERVER]: Error in route /api/addcredit. Log: \n")
        return jsonify({"msg": "Algo ha salido mal"}), 500

@app.route('/api/creditlist', methods=['GET'])
def creditlist():
    try:
        creditlist = Credits.query.all()
        return jsonify([credit.serialize() for credit in creditlist]), 200
    except exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo ha salido mal"}), 500

@app.route ('/api/editcredit/<int:id>', methods=['PUT'])
def editcredit():
    try:
        creditedit = Credits.query.get(id)
        if not creditedit:
            return jsonify({"msg": "Registro no encontrado"}), 404
        
        creditedit.cliente = request.form["cliente"]
        creditedit.monto = request.form["monto"]
        creditedit.tasa_interes = request.form["tasa_interes"]
        creditedit.plazo = request.form["plazo"]
        creditedit.fecha_otorgamiento = request.form["fecha_otorgamiento"]

        db.session.commit()

        return jsonify(creditedit.serializable(), 200)

    except exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo salio mal con la peticion de edición de registro"}), 500 

@app.route ('/api/deletecredit/<int:id>', methods=['DELETE'])
def deletecredit():
    try:
        creditdelete = Credits.query.get(id)
        if not creditdelete:
            return jsonify({"msg": "Registro no encontrado"}), 404
        
        db.session.delete(creditdelete)
        db.session.commit()

        return jsonify({"msg":"Credito eliminado con éxito"}), 200
    
    except exception:
        exception("\n [SERVER]: Error ->")
        return jsonify({"msg":"Algo salió mal al eliminar el registro"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3030)