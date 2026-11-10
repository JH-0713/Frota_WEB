from datetime import timedelta, datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user
from sqlalchemy import select
from routes import *
import os
# gera token
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "VaiCagaRicardo"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

login_manager = LoginManager()
login_manager.login_view = 'login'

login_manager.init_app(app)

class Policial(UserMixin):
    def __init__(self,id_policial, nome,):
        self.id_policial = id_policial
        self.nome = nome

    def get_id(self):
        return str(self.id_policial)

@login_manager.user_loader
def load_user(user_id):
    try:
        lgp1 = get_officer(var_id = user_id)
        if lgp1[1] == 200:
            dados = lgp1[0]
            user_p = Policial(id_policial=dados['id_policial'], nome=dados['nome'])

            return user_p

    except Exception as e:
        print(f'Error: {e}')
        return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/frota', methods=['GET'])
def frota():
    return render_template('frota.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')
        print('form',email, senha)
        if not email or not senha:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('login'))

        try:
            plg1 = login_usuario(email, senha)
            print(f'log_user: {plg1[0]}')

            if plg1[1] == 201:
                dados_p = plg1[0]['user']
                print(f"user: {dados_p}")

                user_l = Policial(id_policial=dados_p['id_policial'], nome=dados_p['nome'])

                login_user(user_l)

                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Usuário ou senha incorretos','danger')
                return redirect(url_for('login'))
        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('login'))

    var_cargos = get_cargo()
    return render_template('login.html', var_cargos=var_cargos)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/listar_policial', methods=['GET','POST'])
def listar_policial():

    var_policial = get_policial()
    var_cargos = get_cargo()

    return render_template('listar_policial.html', var_policial=var_policial,var_cargos=var_cargos)

@app.route('/listar_viatura', methods=['GET'])
def listar_viatura():
    var_modelos = get_modelo()
    var_viatura = get_viatura()
    for i in var_viatura:
        status = i['viatura']['status_atual'].capitalize()
        i['viatura']['status_atual'] = status


    return render_template('listar_viatura.html', var_viatura=var_viatura, var_modelos=var_modelos)

@app.route('/listar_itens', methods=['GET'])
def listar_itens():
    var_itens = get_itens()
    var_categoria = get_categoria()

    for item in var_itens:
        categ_item = item['categoria']['nome_categoria'].replace("_", " ")
        categ_item1 = categ_item.capitalize()
        item['categoria']['nome_categoria'] = categ_item1

    for categ in var_categoria:
        categ1 = categ['nome_categoria'].replace("_", " ").capitalize()
        categ['nome_categoria'] = categ1

    return render_template('listar_itens.html', var_itens=var_itens, var_categoria=var_categoria)



@app.route('/cadastrar_viatura', methods=['GET', 'POST'])
def cadastrar_viatura():
    if request.method == "POST":
        placa = request.form.get('form_placa')
        modelo = request.form.get('form_modelo')
        ano = request.form.get('form_ano')
        km_atual = request.form.get('form_km_atual')

        if not placa or not modelo or not ano or not km_atual or modelo == "None":
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('cadastrar_viatura'))

        try:
            pv1 = post_viatura(placa=placa, modelo=modelo, ano=ano, km_atual=km_atual)
            print(f'pv1: {pv1}')
            if pv1 == 201:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_viatura'))
    var_modelos = get_modelo()
    return render_template('cadastro_viatura.html',var_modelos=var_modelos)

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

            if pp1 == 201:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_policial'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_policial'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_policial'))

    var_cargos = get_cargo()
    for i in var_cargos:
        nome_c = i['nome_cargo'].replace("-", " ")
        nome_c1 = nome_c.replace("_", " ")
        i['nome_cargo'] = nome_c1
    return render_template('cadastro_policial.html',var_cargos=var_cargos)

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

            if pi1 == 201:
                flash("Viatura cadastrada com sucesso!", "success")
                return redirect(url_for('listar_item'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_item'))

        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_item'))

    var_categoria = get_categoria()

    for categ in var_categoria:
        categ1 = categ['nome_categoria'].replace("_", " ").capitalize()
        categ['nome_categoria'] = categ1
    return render_template('cadastro_item.html', var_categoria=var_categoria)

@app.route('/cadastrar_cargo', methods=['POST'])
def cadastrar_cargo():
    if request.method == "POST":
        nome = request.form.get('form_nome')
        categoria = request.form.get('form_categoria')

        if not nome or not categoria:
            flash("Preencha todos os campos", "danger")
            return redirect(request.referrer)

        try:
            pc1 = post_cargo(nome_cargo=nome, categoria=categoria)

            if pc1 == 201:
                flash("Cargo cadastrado com sucesso!", "success")
                return redirect(request.referrer)
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(request.referrer)
        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(request.referrer)

@app.route('/cadastrar_modelo', methods=['POST'])
def cadastrar_modelo():
    if request.method == "POST":
        modelo = request.form.get('form_modelo')
        marca = request.form.get('form_marca')

        if not modelo or not marca:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('cadastrar_viatura'))

        try:
            pm1 = post_modelo(modelo=modelo, marca=marca)

            if pm1 == 201:
                flash("Cargo cadastrado com sucesso!", "success")
                return redirect(url_for('cadastrar_viatura'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('cadastrar_viatura'))
        except Exception as e:
            print(f'Error: {e}')
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('cadastrar_viatura'))




@app.route('/editar_viatura/<var_id>', methods=['POST'])
def editar_viatura(var_id):
    if request.method == "POST":
        placa = request.form.get('form-placa')
        modelo = request.form.get('form-modelo')
        ano = request.form.get('form-ano')
        km_atual = request.form.get('form-odometro')

        if not placa or not modelo or not ano or not km_atual:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_viatura'))
        try:
            put_v1 = put_viatura(placa=placa, ano=ano, km_atual=km_atual, modelo=int(modelo),
                                 var_id=var_id)

            if put_v1 == 200:
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
        cargo = request.form.get('form_cargo')

        if not nome or not email or not cargo:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_policial'))
        try:
            put_p1 = put_policial(nome=nome, email=email, cargo_patente=cargo,
                                 var_id=var_id)

            if put_p1 == 200:
                flash("Policial editada com sucesso", "success")
                return redirect(url_for('listar_policial'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_policial'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_policial'))

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

            if put_r1 == 200:
                flash("Item editada com sucesso", "success")
                return redirect(url_for('listar_responsavel'))
            else:
                flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', "danger")
                return redirect(url_for('listar_responsavel'))

        except Exception as e:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            print(f'Error: {e}')
            return redirect(url_for('listar_responsavel'))

@app.route('/deletar_viatura/<var_id>', methods=['POST'])
def deletar_viatura(var_id):
    if request.method == "POST":
        delete_v1 = delete_viatura(var_id)

        if delete_v1 == 200:
            flash("Viatura deletado com sucesso", "success")
            return redirect(url_for('listar_viatura'))
        else:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('listar_viatura'))

@app.route('/deletar_policial/<var_id>', methods=['POST'])
def deletar_policial(var_id):
    if request.method == "POST":
        delete_r = delete_policial(var_id)
        if delete_r == 200:
            flash("Policial deletado com sucesso", "success")
            return redirect(url_for('listar_policial'))
        else:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('listar_policial'))



@app.route('/pesquisa_viatura', methods=['POST'])
def pesquisa_viatura():
    if request.method == "POST":
        v_text = request.form.get('form_pesquisa')
        if not v_text:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_viatura'))
        elif v_text.isalpha():
            flash("Digite o Prefixo da Viatura", "danger")
            return redirect(url_for('listar_viatura'))

        var_pesquisa_v = pesquisar_viatura(v_text)
        var_modelo = get_modelo()

        print('status', var_pesquisa_v[1])
        if var_pesquisa_v[1] == 200:
            flash(f'Resultado da pesquisa: {v_text}', 'success')
            return render_template('pesquisa_viatura.html',var_viatura=var_pesquisa_v[0],var_modelos=var_modelo)
        elif var_pesquisa_v[1] == 400:
            flash(f'Item não encontrado', 'danger')
            return redirect(url_for('listar_viatura'))
        else:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('listar_viatura'))

@app.route('/pesquisa_itens', methods=['POST'])
def pesquisa_itens():
    if request.method == "POST":
        v_text = request.form.get('form_pesquisa')
        if not v_text:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_itens'))

        var_pesquisa_i = pesquisar_itens(v_text)

        print('status', var_pesquisa_i[1])
        if var_pesquisa_i[1] == 200:
            flash(f'Resultado da pesquisa: {v_text}', 'success')
            return render_template('pesquisa_itens.html',var_itens=var_pesquisa_i[0])
        elif var_pesquisa_i[1] == 400:
            flash(f'Item não encontrado', 'danger')
            return redirect(url_for('listar_itens'))
        else:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('listar_itens'))


@app.route('/pesquisa_policiais', methods=['POST'])
def pesquisa_policiais():
    if request.method == "POST":
        nome = request.form.get('form_pesquisa')
        if not nome:
            flash("Preencha todos os campos", "danger")
            return redirect(url_for('listar_policial'))

        var_pesquisa_p = pesquisar_polical(nome)
        var_cargos = get_cargo()

        print('asd',var_pesquisa_p[0])

        if var_pesquisa_p[1] == 200:
            flash(f'Resultado da pesquisa: {nome}', 'success')

            return render_template('pesquisa_policiais.html',var_policiais=var_pesquisa_p[0], var_cargos=var_cargos)
        elif var_pesquisa_p[1] == 400:
            flash(f'Item não encontrado', 'danger')
            return redirect(url_for('listar_policial'))
        else:
            flash('Falha no Sistema Interno, Tente Novamente mais Tarde.', 'warning')
            return redirect(url_for('listar_policial'))


@app.route('/historicoManutencao')
def historicoManutencao():
    return render_template('historicoManutencao.html')


@app.route('/historicoVeiculo')
def historicoVeiculo():
    return render_template('historicoVeiculo.html')


if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0')