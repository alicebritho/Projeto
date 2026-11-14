from flask import Flask, render_template, request, url_for, redirect, flash
from pathlib import Path
import csv
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

PASTA_DADOS = Path('dados')

def salvar_ponto(nome, endereco, residuo, detalhe, cep, contato):
    PASTA_DADOS.mkdir(exist_ok=True)
    caminho = PASTA_DADOS / 'pontos.csv'
    novo = not caminho.exists()
    campos = ['id', 'nome', 'endereco', 'residuo', 'detalhe', 'cep', 'contato']

    if novo:
        novo_id=1
    else:
        with open(caminho, 'r', newline='', encoding='utf-8') as arquivo_leitura:
            pontos_existentes=list(csv.DictReader(arquivo_leitura))
            novo_id=len(pontos_existentes)+1

    with open(caminho, 'a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if novo: 
            escritor.writeheader() 

        escritor.writerow({
            'id': novo_id,
            'nome': nome,
            'endereco': endereco,
            'residuo': residuo,
            'detalhe': detalhe,
            'cep': cep,
            'contato': contato,
        })

def ler_pontos():
    caminho = PASTA_DADOS / 'pontos.csv'
    if not caminho.exists:
        return[]
    with open(caminho, 'r', newline='', encoding='utf-8') as arquivo:
        return list(csv.DictReader(arquivo))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        residuo = request.form.get('residuo')
        detalhe = request.form.get('detalhe')
        cep = request.form.get('cep')
        contato = request.form.get('contato')

        if not nome or not endereco or not residuo or not cep:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return redirect(url_for('cadastro'))
        
        salvar_ponto(nome, endereco, residuo, detalhe, cep, contato)
        flash('Ponto de coleta cadastrado com sucesso!')
        return redirect(url_for('cadastro'))
    return render_template('cadastro.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pontos=ler_pontos()

    ponto_encontrado = None

    for ponto in pontos:
        if ponto['id'] == str(id):
            ponto_encontrado = ponto
            break
    if ponto_encontrado is None:
        return 'Esse ponto de coleta não existe.', 404

    if request.method == 'POST':
        nome=request.form.get('nome')
        endereco=request.form.get('endereco')
        residuo=request.form.get('residuo')
        detalhe=request.form.get('detalhe')
        cep=request.form.get('cep')
        contato=request.form.get('contato')

        if not nome or not endereco or not residuo or not cep:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return redirect(url_for('editar', id=id))

        atualizar_ponto(id, nome, endereco, residuo, detalhe, cep, contato)
        flash('Ponto de coleta atualizado com sucesso!', 'sucesso')
        return redirect(url_for('editar', id=id))

    return render_template('editar.html', ponto=ponto_encontrado)


def atualizar_ponto(id, nome, endereco, residuo, detalhe, cep, contato):
    caminho = PASTA_DADOS / 'pontos.csv'
    campos = ['id', 'nome', 'endereco', 'residuo', 'detalhe', 'cep', 'contato']
    pontos = ler_pontos()

    for ponto in pontos:
        if ponto['id'] == str(id):
            ponto['nome'] = nome
            ponto['endereco'] = endereco
            ponto['residuo'] = residuo
            ponto['detalhe'] = detalhe
            ponto['cep'] = cep
            ponto['contato'] = contato

    with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(pontos)
