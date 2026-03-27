from itertools import count
from typing import Optional

from flask import Flask, request, jsonify
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel, Field

server = Flask(__name__)
spec = FlaskPydanticSpec('Flask', title='Teste da API')
spec.register(server)

class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int

@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoa)) 
def buscar_pessoas():
    return {'mensagem': 'Programaticamente Falando'}

@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    body = request.context.body.dict()
    return body
    ...

server.run()