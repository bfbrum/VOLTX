from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from voltx import app, db
from models import Instrumentos
from helpers import recupera_imagem, deleta_imagem, FormularioInstrumento
import time

@app.route('/')
def index():
    lista = Instrumentos.query.order_by(Instrumentos.id)
    return render_template('listaInstrumentos.html', titulo='Instrumentos', instrumentos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioInstrumento()
    return render_template('novoInstrumento.html', titulo='Novo Instrumento', form=form)

@app.route('/criar', methods=['POST',])
def criar():

    form = FormularioInstrumento(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    tag = form.tag.data
    nome = form.nome.data
    temperatura = form.temperatura.data
    umidade = form.umidade.data

    instrumento = Instrumentos.query.filter_by(nome=nome).first()

    if instrumento:
        flash('Instrumento já exite!!')
        return redirect(url_for('index'))

    novo_instrumento = Instrumentos(tag=tag, nome=nome, temperatura=temperatura, umidade=umidade)
    db.session.add(novo_instrumento)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/imagem{novo_instrumento.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    instrumento = Instrumentos.query.filter_by(id=id).first()

    form = FormularioInstrumento()
    form.tag.data = instrumento.tag
    form.nome.data = instrumento.nome
    form.temperatura.data = instrumento.temperatura
    form.umidade.data = instrumento.umidade

    capa_instrumento = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Instrumento', id=id, capa_instrumento=capa_instrumento, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():

    form = FormularioInstrumento(request.form)

    if form.validate_on_submit():
        instrumento = Instrumentos.query.filter_by(id=request.form['id']).first()
        instrumento.tag = form.tag.data
        instrumento.nome = form.nome.data
        instrumento.temperatura = form.temperatura.data
        instrumento.umidade = form.umidade.data

        db.session.add(instrumento)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_imagem(instrumento.id)
        arquivo.save(f'{upload_path}/imagem{instrumento.id}-{timestamp}.jpg')

    return redirect( url_for('index'))

@app.route('/deletar/<int:id>')

def deletar(id):

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Instrumentos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Instrumento deletado com sucesso')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

