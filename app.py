from flask import Flask, jsonify, request
import logging
import mysql.connector
from dotenv import dotenv_values
from recursos import get_flight, get_passengers, convert_to_camel

config = dotenv_values(".env")
app = Flask(__name__)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# Objeto para conexión a db
def get_db_connection():
    return mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database=config["DB"],
    )


@app.route("/flights/<int:flight_id>/passengers", methods=["GET"])
def get_passengers_id(flight_id):
    # Intentar conexión con base de datos y handle de errores
    try:
        conn = get_db_connection()
    except mysql.connector.Error as e:
        print(e.msg)
        return jsonify({"code": 400, "errors": "could not connect to db"})

    # Conexión exitosa
    cursor = conn.cursor(dictionary=True)

    # Obtención datos de vuelo
    flight = get_flight(cursor, flight_id)

    # Caso: Vuelo no encontrado
    if not flight:
        return jsonify({"code": 404, "data": {}})

    # Vuelo encontrado
    # Obtener pasajeros
    passengers = get_passengers(cursor, flight_id)

    # Ya no se necesita la conexión
    cursor.close()
    conn.close()

    # Estructurar datos
    data = {
        "code": 200,
        "data": {
            "flight_id": flight["flight_id"],
            "takeoff_date_time": flight["takeoff_date_time"],
            "takeoff_airport": flight["takeoff_airport"],
            "landing_date_time": flight["landing_date_time"],
            "landing_airport": flight["landing_airport"],
            "airplane_id": flight["airplane_id"],
            "passengers": passengers,
        },
    }

    # Convertir snake_case a camelCase
    converted = convert_to_camel(data)

    # Retornar datos solicitados
    return jsonify(converted)


# Logging en consola
@app.before_request
def log_request():
    logger.info(f"{request.remote_addr} {request.method} {request.full_path}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
