from fastapi import Body, FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from auth_jwt import create_jwt_token


app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application",
    version="0.0.1"
)

class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=100)
    director: str = Field(min_length=3),
    category: str = Field(min_length=3 , default="General")
    
movies: List[Movie] = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "category": "Sci-Fi"},
    {"id": 2, "title": "The Dark Knight", "director": "Christopher Nolan", "category": "Action"},
    {"id": 3, "title": "Interstellar", "director": "Christopher Nolan", "category": "Sci-Fi"},
    {"id": 4, "title": "Pulp Fiction", "director": "Quentin Tarantino", "category": "Crime"},
    {"id": 5, "title": "The Matrix", "director": "The Wachowskis", "category": "Sci-Fi"}
]


@app.get("/" ,tags=["inicio"])
def read_root():
    return HTMLResponse(content="<h1>Hello, World!</h1>", status_code=200)


@app.post("/login", tags=["authentication"])
def login(user: User):
    # Aquí deberías validar credenciales con DB, pero de prueba solo generamos el token
    token = create_jwt_token(data={"email": user.email})
    return JSONResponse(content={"access_token": token}, status_code=200)

'''get'''
@app.get("/movies", tags=["Movies"])
def get_movies():
 return JSONResponse(movies, status_code=200)   


'''get by id'''
@app.get("/movies/{movie_id}", tags=["Movies"])
def get_movie(movie_id: int = Path(..., title="The ID of the movie to retrieve", ge=1, le=100)):
    movie = next((m for m in movies if m["id"] == movie_id), None)
    if movie:
        return movie
    return HTMLResponse(content="<h1>Movie not found</h1>", status_code=404)

'''get by params'''
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str = Query(..., min_length=3, max_length=50)):
    filtered_movies = [m for m in movies if m["category"].lower() == category.lower()]
    if filtered_movies:
        return filtered_movies
    return HTMLResponse(content="<h1>No movies found in this category</h1>", status_code=404)


'''POST Method'''
@app.post("/movies", tags=["Movies"])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    director: str = Body(),
    category: str = Body()
):
    new_movie = {"id": id, "title": title, "director": director, "category": category}
    movies.append(new_movie)
    return JSONResponse(new_movie, status_code=201)
   
   
'''PUT Method'''
@app.put("/movies/{movie_id}", tags=["Movies"])
def update_movie(
    movie_id: int,
    title: str = Body(...),
    director: str = Body(...),
    category: str = Body(...)
):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = title
            movie["director"] = director
            movie["category"] = category
            return movie
    return HTMLResponse(content="<h1>Movie not found</h1>", status_code=404)

'''DELETE Method'''
@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    for i, movie in enumerate(movies):
        if movie["id"] == movie_id:
            deleted_movie = movies.pop(i)
            return deleted_movie
    return HTMLResponse(content="<h1>Movie not found</h1>", status_code=404)

