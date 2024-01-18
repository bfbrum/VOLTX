import os
from voltx import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField


class FormularioInstrumento(FlaskForm):
    tag = StringField('Tag', [validators.data_required(), validators.length(min=1, max=20)])
    nome = StringField('Nome', [validators.data_required(), validators.length(min=1, max=50)])
    temperatura = StringField('Temperatura', [validators.data_required(), validators.length(min=1, max=5)])
    umidade = StringField('Umidade', [validators.data_required(), validators.length(min=1, max=10)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'imagem{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_imagem(id):
    imagem = recupera_imagem(id)
    if imagem != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], imagem))