from datetime import timedelta, datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from sqlalchemy import select
from routes import *
import os
# gera token
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VaiCagarRicardo'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/frota', methods=['GET'])
def frota():
    return render_template('frota.html')


@app.route('/listar_policial', methods=['GET'])
def listar_policial():
    var_policial = get_policial()
    return render_template('listar_policial.html', var_policial=var_policial[0])


@app.route('/listar_responsavel', methods=['GET'])
def listar_responsavel():
    var_responsavel = get_responsavel()
    print("Responsavel:", var_responsavel)
    return render_template('listar_responsavel.html', var_responsavel=var_responsavel[0])


@app.route('/listar_viatura', methods=['GET'])
def listar_viatura():
    var_viatura = get_viatura()
    return render_template('listar_viatura.html', var_viatura=var_viatura[0])


@app.route('/listar_itens', methods=['GET'])
def listar_itens():
    var_itens = get_itens()
    return render_template('listar_itens.html', var_itens=var_itens[0])


@app.route('/cadastrar_viatura', methods=['GET', 'POST'])
def cadastrar_viatura():
    if request.method == "POST":
        placa = request.form.get('form_placa')
        modelo = request.form.get('form_modelo')
        ano = request.form.get('form_ano')
        km_atual = request.form.get('form_km_atual')
        status_atual = request.form.get('form_status')
        print(placa, modelo, ano, km_atual, status_atual)

        if not placa or not modelo or not ano or not km_atual or not status_atual:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('cadastrar_viatura'))

        try:
            pv1 = post_viatura(placa=placa, modelo=modelo, ano=ano, km_atual=km_atual, status_atual=status_atual)

            if pv1[1] == 200:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_viatura'))

    return render_template('cadastro_viatura.html')


@app.route('/cadastrar_policial', methods=['GET', 'POST'])
def cadastrar_policial():
    if request.method == "POST":
        nome = request.form.get('form_nome')
        email = request.form.get('form_email')
        senha = request.form.get('form_senha')
        cargo = request.form.get('form_cargo')

        if not nome or not email or not senha or not cargo:
            print('error: valores inválidos')
            flash("Digite em todos os campos", "danger")
            return redirect(url_for('cadastrar_policial'))

        try:
            pp1 = post_policial(nome=nome, email=email, senha=senha,cargo_patente=cargo)

            if pp1[1] == 200:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_responsavel'))

    return render_template('cadastro_policial.html')


@app.route('/cadastrar_responsavel', methods=['GET', 'POST'])
def cadastrar_responsavel():
    if request.method == "POST":
        nome = request.form.get('form_nome')
        email = request.form.get('form_email')
        cargo = request.form.get('form_cargo_funcao')
        senha = request.form.get('form_senha')

        print(nome, email, cargo, senha)

        if not nome or not email or not cargo or not senha:
            print("error: valores inválidos")
            flash("Digite em todos os campos", "danger")
            return redirect(url_for('cadastrar_responsavel'))

        try:
            pr1 = post_responsavel(nome=nome, cargo_funcao=cargo, email=email, senha=senha)

            if pr1[1] == 200:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_responsavel'))

    return render_template('cadastro_responsavel.html')


@app.route('/cadastrar_item', methods=['GET', 'POST'])
def cadastrar_item():
    if request.method == "POST":
        nome = request.form.get('form_nome')
        descricao = request.form.get('form_descricao')
        categoria = request.form.get('form_categoria')
        valor_unitario = request.form.get('form_valor')

        if not nome or not descricao or not categoria or not valor_unitario or categoria == "none":
            print('error: valores invalidos')
            flash("Digite em todos os campos", 'danger')
            return redirect(url_for('cadastrar_item'))

        try:
            pi1 = post_item(nome_item=nome, descricao=descricao, categoria_falha=categoria, valor_unitario=valor_unitario)

            if pi1[1] == 200:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_item'))

    return render_template('cadastro_item.html')

@app.route('/editar_viatura/<var_id>', methods=['POST'])
def editar_viatura(var_id):
    if request.method == "POST":
        placa = request.form.get('form_placa')
        modelo = request.form.get('form_modelo')
        ano = request.form.get('form_ano')
        km_atual = request.form.get('form_km_atual')
        status_atual = request.form.get('form_status')

        if not placa or not modelo or not ano or not km_atual or not status_atual:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_viatura'))
        try:
            put_v1 = put_viatura(placa=placa, ano=ano, km_atual=km_atual, modelo=modelo, status_atual=status_atual,
                                 var_id=var_id)

            if put_v1[1] == 200:
                flash("Viatura editada com sucesso", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_viatura'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_viatura'))

@app.route('/editar_policial/<var_id>', methods=['POST'])
def editar_policial(var_id):
    if request.method == "POST":
        nome = request.form.get('form_nome')
        email = request.form.get('form_email')
        senha = request.form.get('form_senha')
        cargo = request.form.get('form_cargo')

        if not nome or not email or not senha or not cargo:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_policial'))
        try:
            put_p1 = put_policial(nome=nome, email=email, senha=senha, cargo_patente=cargo,
                                 var_id=var_id)

            if put_p1[1] == 200:
                flash("Policial editada com sucesso", "success")
                return redirect(url_for('listar_policial'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_policial'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_policial'))

@app.route('/editar_responsavel/<var_id>', methods=['POST'])
def editar_responsavel(var_id):
    if request.method == "POST":
        nome = request.form.get('form_nome')
        email = request.form.get('form_email')
        senha = request.form.get('form_senha')
        cargo = request.form.get('form_cargo')

        if not nome or not email or not senha or not cargo:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_responsavel'))
        try:
            put_r1 = put_responsavel(nome=nome, email=email, senha=senha, cargo_funcao=cargo,
                                 var_id=var_id)

            if put_r1[1] == 200:
                flash("Responsavel editada com sucesso", "success")
                return redirect(url_for('listar_responsavel'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_responsavel'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_responsavel'))

@app.route('/editar_item/<var_id>', methods=['POST'])
def editar_item(var_id):
    if request.method == "POST":
        nome = request.form.get('form_nome')
        descricao = request.form.get('form_descricao')
        categoria = request.form.get('form_categoria')
        valor = request.form.get('form_valor')

        if not nome or not descricao or not categoria or not valor:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_responsavel'))
        try:
            put_r1 = put_item(nome_item=nome, descricao=descricao, categoria=categoria, valor_unitario=valor,
                                 var_id=var_id)

            if put_r1[1] == 200:
                flash("Item editada com sucesso", "success")
                return redirect(url_for('listar_responsavel'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_responsavel'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_responsavel'))

@app.route('/historicoManutencao')
def historicoManutencao():
    return render_template('historicoManutencao.html')


@app.route('/historicoVeiculo')
def historicoVeiculo():
    return render_template('historicoVeiculo.html')


if __name__ == '__main__':
    app.run(debug=True, port=5008, host='0.0.0.0')