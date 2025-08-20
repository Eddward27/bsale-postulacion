from collections import defaultdict
from modelos import (
    get_boarding_passes_from_id,
    get_passengers_from_id,
    get_flight_from_id,
    get_seats_from_id,
)


# Convertir snake_case a camelCase
def to_camel_case(string):
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


# Solución recursiva para transformar keys de obj a camelCase
def convert_to_camel(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_key = to_camel_case(k)
            new_obj[new_key] = convert_to_camel(v)
        return new_obj
    elif isinstance(obj, list):
        return [convert_to_camel(item) for item in obj]
    else:
        return obj


# Obtener los datos de vuelo según flight_id
def get_flight(cursor, flight_id):
    flight = get_flight_from_id(cursor, flight_id)
    return flight


# Obtener los datos de pasajeros según flight_id
def get_passengers(cursor, flight_id):
    # Obtener datos de boarding_passes
    boarding_passes = get_boarding_passes_from_id(cursor, flight_id)

    # Obtener listado de passenger_id para listado de passenger
    passenger_ids = []
    for item in boarding_passes:
        passenger_ids.append(item["passenger_id"])

    # Obtener todos los passenger del vuelo según passenger_id
    passengers = get_passengers_from_id(cursor, passenger_ids)
    seats = get_seats_from_id(cursor, flight_id)

    # Agregar datos extras para procesamiento a obj
    extra_data = {item["passenger_id"]: item for item in boarding_passes}
    for p in passengers:
        if p["passenger_id"] in extra_data:
            p["boarding_pass_id"] = extra_data[p["passenger_id"]].get(
                "boarding_pass_id"
            )
            p["purchase_id"] = extra_data[p["passenger_id"]].get("purchase_id")
            p["seat_type_id"] = extra_data[p["passenger_id"]].get("seat_type_id")

    # Asignación de seat a passenger
    passengers = assign_seats(passengers, seats)

    # Retornar obj de passengers
    return passengers


def assign_seats(passengers, seats):
    # Organizar seats por seat_type_id y row/column
    available_seats = defaultdict(list)
    for seat in seats:
        available_seats[seat["seat_type_id"]].append(seat)
    for av_seat in available_seats:
        available_seats[av_seat].sort(key=lambda s: (s["seat_row"], s["seat_column"]))

    # Agrupar passengers según purchase_id
    groups = defaultdict(list)
    for p in passengers:
        groups[p["purchase_id"]].append(p)

    # Asignación de grupos
    def assign_group(group):
        # Clasificar passengers según age
        underage = [p for p in group if p["age"] < 18]
        adults = [p for p in group if p["age"] >= 18]

        # Asignación
        for child in underage:
            paired = False
            for adult in adults:
                seat_list = available_seats[adult["seat_type_id"]]
                if seat_list:
                    # Asignar seat a passenger adulto
                    seat = seat_list.pop(0)
                    adult["seat_id"] = seat["seat_id"]

                    # Intentar asignar menor junto a su familia
                    family_seats = [
                        s
                        for s in available_seats[child["seat_type_id"]]
                        if s["seat_row"] == seat["seat_row"]
                    ]
                    if family_seats:
                        child_seat = family_seats.pop(0)
                        available_seats[child["seat_type_id"]].remove(child_seat)
                        child["seat_id"] = child_seat["seat_id"]
                    else:
                        # Asignación no lograda -> Primer asiento disponible
                        if available_seats[child["seat_type_id"]]:
                            child_seat = available_seats[child["seat_type_id"]].pop(0)
                            child["seat_id"] = child_seat["seat_id"]

                    adults.remove(adult)
                    paired = True
                    break

            if available_seats[child["seat_type_id"]] and not paired:
                child_seat = available_seats[child["seat_type_id"]].pop(0)
                child["seat_id"] = child_seat["seat_id"]

        # Asignar el resto
        for p in group:
            if "seat_id" not in p and available_seats[p["seat_type_id"]]:
                seat = available_seats[p["seat_type_id"]].pop(0)
                p["seat_id"] = seat["seat_id"]

    # Ejecutar asignación para cada grupo
    for group in groups.values():
        assign_group(group)

    return passengers
