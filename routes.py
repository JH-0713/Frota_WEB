import requests
#
endereco = "http://10.135.232.24:5005"

def get_policial():
    url = f"{endereco}/get_policiais"

    result_policia = requests.get(url)

    return result_policia.json()

def post_policial(nome,email,senha,cargo_patente,matricula):
    url = f"{endereco}/post_policial"
#
    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cargo_patente": cargo_patente,
        "matricula": matricula
    }

    result_policia = requests.post(url=url, json=dados)

    return result_policia.json()

def get_viatura():
    url = f"{endereco}/get_viaturas"

    result_viatura = requests.get(url)

    return result_viatura.json()


def post_viatura(placa, ano, km_atual,modelo, status_atual):
    url = f"{endereco}/post_viatura"


    dados = {
        "placa": placa,
        "ano":ano,
        "km_atual": km_atual,
        "modelo": modelo,
        "status_atual": status_atual

    }


    result_policia = requests.post(url=url, json=dados)

    return result_policia.json()

def get_responsavel():
    url = f"{endereco}/get_responsaveis"

    result_responsavel = requests.get(url)

    print("Responsavel:",result_responsavel)

    return result_responsavel.json()



def post_responsavel(nome,email,senha,cargo_funcao):
    url = f"{endereco}/post_responsavel"

    dados = {
        "nome":nome,
        "email":email,
        "senha":senha,
        "cargo_funcao":cargo_funcao

    }

    result_listarResponsavel = requests.post(url, json=dados)

    return result_listarResponsavel.json()



def get_itens():
    url = f"{endereco}/get_itens"

    result_listarItemManutencao = requests.get(url)


    return result_listarItemManutencao.json()




def post_item(nome_item,descricao,categoria_falha,valor_unitario):

    url = f"{endereco}/post_itens_manutencao"

    dados = {
        "nome_item":nome_item,
        "descricao":descricao,
        "categoria_falha":categoria_falha,
        "valor_unitario":valor_unitario

    }

    result_listarItemManutencao = requests.post(url, json=dados)

    return result_listarItemManutencao.json()