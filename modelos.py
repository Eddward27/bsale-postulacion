# Obtener los datos de vuelo según flight_id
def get_flight_from_id(cursor, flight_id):
    cursor.execute(f"SELECT * FROM flight WHERE flight_id = {str(flight_id)}")
    flight = cursor.fetchone()
    return flight


# Obtener los datos de asientos según flight_id
def get_seats_from_id(cursor, airplane_id):
    cursor.execute(f"SELECT * FROM seat WHERE airplane_id = {str(airplane_id)}")
    seats = cursor.fetchall()
    return seats


# Obtener los datos de boarding_pass según flight_id
def get_boarding_passes_from_id(cursor, flight_id):
    cursor.execute(
        f"SELECT passenger_id, boarding_pass_id, purchase_id, seat_type_id FROM boarding_pass WHERE flight_id = {str(flight_id)}"
    )
    boarding_passes = cursor.fetchall()
    return boarding_passes


# Obtener los datos de passenger según flight_id
def get_passengers_from_id(cursor, passenger_ids):
    placeholders = ",".join(["%s"] * len(passenger_ids))
    cursor.execute(
        f"SELECT * FROM passenger WHERE passenger_id IN ({placeholders})", passenger_ids
    )
    passengers = cursor.fetchall()
    return passengers
