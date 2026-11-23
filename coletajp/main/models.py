#estrutura de banco de dados

import csv
from pathlib import Path

PASTA_DADOS = Path('dados')

#cria o ponto

def salvar_ponto(ativo, nome, endereco, residuo, detalhe, cep, contato):
    PASTA_DADOS.mkdir(exist_ok=True)
    caminho = PASTA_DADOS / 'pontos.csv'
    novo = not caminho.exists()
    campos = ['ativo', 'id', 'nome', 'endereco', 'residuo', 'detalhe', 'cep', 'contato']

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
            'ativo': True,
            'id': novo_id,
            'nome': nome,
            'endereco': endereco,
            'residuo': residuo,
            'detalhe': detalhe,
            'cep': cep,
            'contato': contato,
        })

#leitura dos pontos

def ler_pontos():
    caminho = PASTA_DADOS / 'pontos.csv'
    if not caminho.exists:
        return[]
    with open(caminho, 'r', newline='', encoding='utf-8') as arquivo:
        pontos = list(csv.DictReader(arquivo))
    for ponto in pontos:
      ponto['ativo'] = ponto.get('ativo', 'True') == 'True'
    return pontos

#atualizar dados do ponto

def atualizar_ponto(ativo, id, nome, endereco, residuo, detalhe, cep, contato):
    caminho = PASTA_DADOS / 'pontos.csv'
    campos = ['ativo', 'id', 'nome', 'endereco', 'residuo', 'detalhe', 'cep', 'contato']
    pontos = ler_pontos()

    for ponto in pontos:
        if ponto['id'] == str(id):
            ponto['ativo'] = ativo
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

    