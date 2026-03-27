from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec, Response
from pydantic import BaseModel

server = Flask(__name__)
spec = FlaskPydanticSpec('Flask', title='Teste da API')
spec.register(server)

class MensagemRetorno(BaseModel):
    mensagem: str

@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=MensagemRetorno)) 
def buscar_pessoas():
    return {'mensagem': 'Programaticamente Falando'}

server.run()