import requests

endereco = "http://10.135.232.10:5002"

def get_policial():
    url = f"{endereco}/get_policiais"

    result_policia = requests.get(url)

    return result_policia.json()

def get_viatura():
    url = f"{endereco}/get_viaturas"

    result_viatura = requests.get(url)

    return result_viatura.json()

def get_responsavel():
    url = f"{endereco}/get_responsaveis"

    result_responsavel = requests.get(url)

    return result_responsavel.json()

def get_itens():
    url = f"{endereco}/get_itens"

    result_item = requests.get(url)

    return result_item.json()

def get_modelo():
    url = f"{endereco}/get_carros"

    result_modelo = requests.get(url)

    return result_modelo.json()

def get_cargo():
    url = f"{endereco}/get_cargos"

    result_modelo = requests.get(url)

    return result_modelo.json()


def post_policial(nome,email,senha,cargo_patente):
    url = f"{endereco}/post_policial"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cargo_patente": cargo_patente,
    }

    result_policia = requests.post(url=url, json=dados)

    return result_policia.status_code

def post_viatura(placa, ano, km_atual,modelo):
    url = f"{endereco}/post_viatura"

    dados = {
        "placa": placa,
        "ano":ano,
        "km_atual": km_atual,
        "modelo": modelo,

    }

    result_viatura = requests.post(url=url, json=dados)

    return result_viatura.status_code

def post_responsavel(nome,email,senha,cargo_funcao):
    url = f"{endereco}/post_responsavel"

    dados = {
        "nome":nome,
        "email":email,
        "senha":senha,
        "cargo_funcao":cargo_funcao

    }

    result_responsavel = requests.post(url, json=dados)

    return result_responsavel.status_code

def post_item(nome_item,descricao,categoria_falha,valor_unitario):

    url = f"{endereco}/post_itens_manutencao"

    dados = {
        "nome_item":nome_item,
        "descricao":descricao,
        "categoria_falha":categoria_falha,
        "valor_unitario":valor_unitario

    }

    result_item = requests.post(url, json=dados)

    return result_item.status_code


def pesquisar_polical(matricula):
    url = f"{endereco}/pesquisar_policial"

    dados = {
        "matricula": matricula
    }

    result_policial = requests.post(url=url, json=dados)

    return result_policial.json(), result_policial.status_code

def pesquisar_viatura(prefixo):
    url = f"{endereco}/pesquisar_viatura"

    dados = {
        "prefixo": prefixo
    }

    result_policial = requests.post(url=url, json=dados)

    return result_policial.json(), result_policial.status_code

def pesquisar_itens(nome):
    url = f"{endereco}/pesquisar_itens"

    dados = {
        "nome_item": nome
    }

    result_policial = requests.post(url=url, json=dados)

    return result_policial.json(), result_policial.status_code





def put_policial(nome, email, senha,cargo_patente,var_id):
    url = f"{endereco}/put_policial/{var_id}"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cargo_patente": cargo_patente,
    }

    result_policial = requests.put(url=url, json=dados)

    return result_policial.json(), result_policial.status_code

def put_viatura(placa, ano, km_atual,modelo,var_id):
    url = f"{endereco}/put_viatura/{var_id}"

    dados = {
        "placa": placa,
        "ano":ano,
        "km_atual": km_atual,
        "modelo": modelo,
    }

    result_viatura = requests.put(url=url, json=dados)

    return result_viatura.status_code

def put_responsavel(nome,email,senha,cargo_funcao,var_id):
    url = f"{endereco}/put_responsavel/{var_id}"

    dados = {
        "nome":nome,
        "email":email,
        "senha":senha,
        "cargo_funcao":cargo_funcao
    }

    result_responsavel = requests.put(url=url, json=dados)

    return result_responsavel.status_code

def put_item(nome_item, descricao, categoria, valor_unitario, var_id):
    url = f"{endereco}/put_item_manutencao/{var_id}"

    dados = {
        "nome_item": nome_item,
        "descricao": descricao,
        "categoria": categoria,
        "valor_unitario": valor_unitario
    }

    result_item = requests.put(url=url, json=dados)

    return result_item.status_code



def delete_policial(var_id):
    url = f"{endereco}/delete_policial/{var_id}"

    result_viatura = requests.delete(url)

    return result_viatura.status_code

def delete_viatura(var_id):
    url = f"{endereco}/delete_viatura/{var_id}"

    result_viatura = requests.delete(url)

    return result_viatura.status_code

def delete_responsavel(var_id):
    url = f"{endereco}/delete_responsavel/{var_id}"

    result_viatura = requests.delete(url)

    return result_viatura.status_code

def delete_item(var_id):
    url = f"{endereco}/delete_item/{var_id}"

    result_viatura = requests.delete(url)

    return result_viatura.status_code