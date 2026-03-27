from itertools import count
from typing import Optional

from flask import Flask, request, jsonify
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('Flask', title='Teste da API')
spec.register(server)
database = TinyDB('database.json')

class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int

@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoa)) 
def buscar_pessoas():
    """Retorna todas as pessoas da base de dados."""
    return jsonify(database.all())

@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    """Insere pessoa no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body
    ...

server.run()