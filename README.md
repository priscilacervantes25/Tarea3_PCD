# Tarea3_PCD

## 📚 Users API

API REST en **FastAPI** para gestionar usuarios, con seguridad mediante **API Key** y persistencia en **SQLite**.

---

## 🚀 Instalación

### Crear entorno

uv venv

### Instalar dependencias

uv pip install fastapi uvicorn sqlalchemy python-dotenv pydantic

### ⚙️ Variables de entorno

Definir '.env': API_KEY=contra
.env.example(para cuando alguien clone el repo, deba poner un apikey)

### ▶️ Correr la app

Para poder correr la app debemos de ejecutar lo siguiente en la terminal: uv run fastapi dev main.py

---
## 📌 Descripción Endpoints 

Todos los endpoints deben de tener un header por seguridad 

Empezamos con los endpoints:

1. Crear usuario 'post'

2. Actualizar usuario 'put'

3. Obtener usuario 'get'

4. Eliminar usario 'delete'

Se crea un user para el modelo donde podemos encontrar las variables *user_name*, *user_id*, *user_email*, *age*, *recommendations* and *ZIP*

Un ejemplo de requests sería como lo siguiente:


POST:

{
  "user_name": "pris",
  "user_id": 0,
  "user_email": "pris@gmail.com",
  "age": 20,
  "recommendations": ["apple"],
  "ZIP": "1234"
}

PUT:

{
  "user_name": "priscila",
  "user_id": 0,
  "user_email": "pris@gmail.com",
  "age": 20,
  "recommendations": ["apple"],
  "ZIP": "1234"
}

GET:

Response body

{
  "age": 20,
  "user_id": 0,
  "ZIP": "1234",
  "user_name": "priscila",
  "user_email": "pris@gmail.com",
  "recommendations": "apple"
}

DELETE:

	
Response body

{
  "deleted_id": 0
}




## 📂 Estructura del proyecto

.
├── main.py

├── models.py

├── database.py

├── users.db

├── .env

├── .env.example

└── README.md

**Dos** ramas, main la princiapl y **feat/api**













