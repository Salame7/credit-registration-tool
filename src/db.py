from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Creditos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String)
    monto = db.Column(db.Float)
    tasa_interes = db.Column(db.Float)
    plazo = db.Column(db.Integer)
    fecha_otorgamiento = db.Column(db.String)

    def __init__(user, cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
        super().__init__()
        user.cliente = cliente
        user.monto = monto
        user.tasa_interes = tasa_interes
        user.plazo = plazo
        user.fecha_otorgamiento = fecha_otorgamiento

    def __str__(user):
        return "\nCliente : {}. Monto: {}. Tasa de interes: {}. Plazo: {}. Fecha de otorgamiento: {}.\n".format(
            user.cliente,
            user.monto,
            user.tasa_interes,
            user.plazo,
            user.fecha_otorgamiento
        )
    
    def serialize(user):
        return {
            "id": user.id,
            "cliente": user.cliente,
            "monto": user.monto,
            "tasa_interes": user.tasa_interes,
            "plazo": user.plazo,
            "fecha_otorgamiento": user.fecha_otorgamiento
        }