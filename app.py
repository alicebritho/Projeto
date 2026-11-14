from flask import Flask, render_template, request, url_for, redirect
from pathlib import Path
import csv

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

PASTA_DADOS = Path('dados')

def salvar_ponto(nome, endereco, residuo, detalhe, cep, contato):
    PASTA_DADOS.mkdir(exist_ok=True)
    caminho = PASTA_DADOS / 'pontos.csv'
    novo = not caminho.exists()
    campos = ['nome', 'endereco', 'residuo', 'detalhe', 'cep', 'contato']

    with open(caminho, 'a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if novo: 
            escritor.writeheader() 
        escritor.writerow({
            'nome': nome,
            'endereco': endereco,
            'residuo': residuo,
            'detalhe': detalhe,
            'cep': cep,
            'contato': contato,
        })

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        residuo = request.form.get('residuo')
        detalhe = request.form.get('detalhe')
        cep = request.form.get('cep')
        contato = request.form.get('contato')
        
        salvar_ponto(nome, endereco, residuo, detalhe, cep, contato)
        return redirect(url_for('cadastro'))
    return render_template('cadastro.html')

if __name__ == "__main__":
    app.run(debug=True)