from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_z.routers import auth, todo, user
from fastapi_z.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá mundo!'}


# Exercicio aula 02
@app.get('/ola_mundo/', response_class=HTMLResponse)
def ola_mundo():
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
