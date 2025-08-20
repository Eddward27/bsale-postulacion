# Bsale Postulación – API de Check-In Automático

Este proyecto implementa una **API REST en Python con Flask** que simula el proceso de **check-in automático de pasajeros en vuelos**.  
La API se conecta a una base de datos MySQL y expone un endpoint que entrega la información de un vuelo junto con sus pasajeros y asientos asignados.

---

## Funcionalidad

-   **Endpoint principal:**

    ```
    GET /flights/<flight_id>/passengers
    ```

    -   Disponible en `https://api-bsale.elwarizapo.com/flights/<flight_id>/passengers`
    -   Retorna la información de un vuelo y sus pasajeros.
    -   Incluye datos de asientos asignados de acuerdo a reglas:
        -   Se agrupan pasajeros por **purchase_id** (compra en conjunto).
        -   Menores de edad se asignan lo más cerca posible a un adulto del mismo grupo.
        -   Si no hay asientos contiguos disponibles, se asigna el primer asiento libre.

-   **Casos contemplados:**
    -   ✅ Vuelo encontrado → Retorna `200` con la información del vuelo y pasajeros.
    -   ❌ Vuelo no encontrado → Retorna `404`.
    -   ⚠️ Error de conexión a la base de datos → Retorna `400`.

---

## Estructura del proyecto

```
.
├── app.py            # API Flask principal
├── recursos.py       # Funciones de negocio (camelCase, asignación de asientos, etc.)
├── modelos.py        # Funciones de acceso a la base de datos
├── .env              # Variables de entorno (credenciales DB)
└── requirements.txt  # Dependencias del proyecto
```

---

## Ejemplo de respuesta

### Request:

```
GET /flights/1/passengers
```

### Response:

```json
{
  "code": 200,
  "data": {
    "flightId": 1,
    "takeoffDateTime": 1688207580,
    "takeoffAirport": "Aeropuerto Internacional Arturo Merino Benitez, Chile",
    "landingDateTime": 1688221980,
    "landingAirport": "Aeropuerto Internacional Jorge Cháve, Perú",
    "airplaneId": 1,
    "passengers": [
      {
        "passengerId": 90,
        "dni": 983834822,
        "name": "Marisol",
        "age": 44,
        "country": "México",
        "boardingPassId": 24,
        "purchaseId": 47,
        "seatTypeId": 1,
        "seatId": 1
      },
      { ... }
    ]
  }
}
```

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Eddward27/bsale-postulacion.git
cd bsale-postulacion
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con tus credenciales de base de datos:

```env
HOST=localhost
USER=root
PASSWORD=tu_password
DB=bsale_airline
```

### 5. Ejecutar la API

```bash
python app.py
```

La API quedará disponible en:

```
http://localhost:8000
```

---

## Dependencias principales

-   **Flask** → Framework web.
-   **mysql-connector-python** → Conexión a base de datos MySQL.
-   **python-dotenv** → Manejo de variables de entorno.

---

## Explicación de la solución

1. **Conexión a DB:**  
   `app.py` utiliza `mysql.connector` para conectarse a la base de datos usando credenciales de `.env`.

2. **Obtención de datos:**

    - `modelos.py` abstrae consultas SQL (`flight`, `seat`, `boarding_pass`, `passenger`).
    - `recursos.py` orquesta la obtención de la información completa de un vuelo.

3. **Procesamiento de pasajeros:**

    - Los pasajeros se agrupan por compra (`purchase_id`).
    - Se asignan asientos según disponibilidad y cercanía familiar (menores acompañados de adultos).

4. **Formato de respuesta:**
    - Toda la información se transforma de `snake_case` a `camelCase` usando `convert_to_camel`.
    - Se retorna en formato **JSON** estandarizado.

---

**Autor:** Matías Allende – Postulación Bsale
