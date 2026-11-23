#rotas do site

from flask import render_template, url_for, request, redirect, flash
from . import app, models
import os

#homepage

@app.route("/")
def homepage():
    return render_template("index.html")

#mapa

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

#SAC

@app.route("/duvidas")
def duvidas():
    return render_template("duvidas.html")

#configurações

@app.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")

#cadastro de usuário

@app.route("/cadastro-usuario", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "email": request.form["email"],
            "senha": request.form["senha"],
            "confirmar_senha": request.form["confirmar_senha"],
            "perfil": request.form["perfil"],
            }

    return render_template("cadastro-usuario.html")

#login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dados = {

            "usuario": request.form["usuario"],
            "senha": request.form["senha"],
            }

        #task de validação aqui

        #task de armazenamento aqui

    return render_template("login.html")

#cadastro de ponto

@app.route('/cadastro-ponto', methods=['GET', 'POST'])
def cadastro_ponto():
    if request.method == 'POST':
        ativo = True
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        residuo = request.form.get('residuo')
        detalhe = request.form.get('detalhe')
        cep = request.form.get('cep')
        contato = request.form.get('contato')

        if not nome or not endereco or not residuo or not cep:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return redirect(url_for('cadastro_ponto'))
        
        models.salvar_ponto(ativo, nome, endereco, residuo, detalhe, cep, contato)
        flash('Ponto de coleta cadastrado com sucesso!')
        return redirect(url_for('cadastro_ponto'))
    return render_template('cadastro-ponto.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pontos=models.ler_pontos()

    ponto_encontrado = None

    for ponto in pontos:
        if ponto['id'] == str(id):
            ponto_encontrado = ponto
            break
    if ponto_encontrado is None:
        return 'Esse ponto de coleta não existe.', 404

    if request.method == 'POST':
        ativo=request.form.get('ativo') == 'True'
        nome=request.form.get('nome')
        endereco=request.form.get('endereco')
        residuo=request.form.get('residuo')
        detalhe=request.form.get('detalhe')
        cep=request.form.get('cep')
        contato=request.form.get('contato')

        if not nome or not endereco or not residuo or not cep:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return redirect(url_for('editar', id=id))

        models.atualizar_ponto(ativo, id, nome, endereco, residuo, detalhe, cep, contato)
        flash('Ponto de coleta atualizado com sucesso!', 'sucesso')
        return redirect(url_for('editar', id=id))

    return render_template('editar-ponto.html', ponto=ponto_encontrado)