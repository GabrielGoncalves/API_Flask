from itertools import count
from typing import Optional

from flask import Flask, request, jsonify
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('Flask', title='API com Flask')
spec.register(server)
database = TinyDB('database.json')
pessoa_id = count()


class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(pessoa_id))
    nome: str
    idade: int

class Pessoas(BaseModel):
    pessoas: list[Pessoa]
    count: int

@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas)) 
def buscar_pessoas():
    """Retorna todas as pessoas da base de dados."""
    return jsonify(
        Pessoas(pessoas=database.all(),
                count=len(database.all())
                ).dict()
    )

@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    """Insere pessoa no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body

@server.put('/pessoas/<int:id>')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def altera_pessoa(id):
    Pessoa = Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id == id)
    return jsonify(body)

@server.delete('/pessoas/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deleta_pessoa(id):
    """Remove uma pessoa do banco de dados"""
    Pessoa = Query()
    database.remove(Pessoa.id == id)
    return jsonify({})

server.run()