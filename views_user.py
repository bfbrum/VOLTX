from flask import request, render_template, flash, session, redirect, url_for
from voltx import app
from helpers import FormularioUsuario
from models import Usuarios
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', titulo= 'Faça seu Login',proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    #processode autenticação criptografado através do Bcrypt
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

#@app.route('/novo_usuario', methods=['POST',])
#def novo_usuario():
    #form = FormUser(request.form)
    #nome = form.nome.data
    #idade = form.idade.data
    #senha = generate_password_hash(form.senha.data).decode('utf-8')

    #new_user = Usuarios(nome=nome, idade=idade, senha=senha)
    #db.session.add(new_user)
    #db.session.commit()
