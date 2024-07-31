# API REST STARWARS BACKEND
### Este proyecto proporciona una API REST para un blog temático de Star Wars, permitiendo gestionar planetas, personajes y favoritos. Hecho para 4GeeksAcademy, basado en [Starwars API](https://swapi.tech/)

## INSTALAR (pipenv)
clonar repositorio
1. Instalar pipenv si no lo tienes:
```shell 
pip install pipenv
```
2. Crear un entorno virtual e instalar las dependencias:
```shell
pipenv install
```
3. Activar el entorno virtual:
```shell
pipenv shell
```
## INSTALAR (base de datos)
1. Inicializar el repositorio de migraciones:
```shell
flask db init
```
2. Crear una migración inicial:
```shell
flask db migrate -m "Initial migration"
```
3. Aplicar la migración a la base de datos:
```shell
flask db upgrade
```
# Ejecutar la aplicación:
```shell
flask run
```
## ENDPOINTS

### Usuarios
- POST/GET /users
-- Request Body (JSON):
```shell
{
  "username": "example",
  "email": "example@example.com",
  "admin": false,
  "active": true
}
```
### planets o People
- GET /people o planet

#### Crear una nueva persona:
- POST /people
- Request Body (JSON):
```shell
{
  "name": "Luke Skywalker",
  "categoria_type": "Jedi",
  "birth_year": "19BBY",
  "eye_color": "Blue",
  "gender": "Male",
  "hair_color": "Blond",
  "height": "172",
  "mass": "77",
  "skin_color": "Fair",
  "homeworld_id": 1,
  "species": "Human",
  "starships": "X-wing",
  "vehicles": "Landspeeder"
}
```
#### Crear un nuevo planeta:
- POST /planet
- Request Body (JSON):
```shell
{
  "name": "Tatooine",
  "categoria_type": "Desert",
  "climate": "Arid",
  "diameter": "10465",
  "gravity": "1 standard",
  "orbital_period": "304",
  "population": "200000",
  "rotation_period": "23",
  "surface_water": "1",
  "terrain": "Desert"
}
```
#### Eliminar una planet o people:
- DELETE /people/<int:id>
- DELETE /planet/<int:id>

### Favoritos
#### Obtener favoritos de un usuario:
- GET /user/favorites
- Query Params:
- user_id (requerido): ID del usuario

#### Añadir un favorito (persona o planeta):
- POST /favorite/people/<int:people_id>
- POST /favorite/planet/<int:planet_id>
- Request Body (JSON):
```shell
{
  "user_id": 1
}
```
#### Eliminar un favorito (persona o planeta):
- DELETE /favorite/people/<int:people_id>
- DELETE /favorite/planet/<int:planet_id>
- Request Body (JSON):
```shell
{
  "user_id": 1
}
```
