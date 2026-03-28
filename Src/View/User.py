from flask import Blueprint, render_template, request, flash, redirect, url_for
from Src.Controller.Users import UserController
from Src.Model.BancoDados import Usuarios
from flask_login import login_required
from config import admin_required
from Src.Model import Regex
from werkzeug.security import generate_password_hash

User = Blueprint('user', __name__)


@User.route('/list', defaults={'page': 1}, methods=['GET'])
@User.route('/list/<int:page>', methods=['GET'])
@login_required
def listUser(page):
    _userFilter = request.values.get('nomeUsuario')
    if _userFilter == 'None' or _userFilter is None:
        _userFilter = ""
    return render_template('listaUsuarios.html', listData=UserController.List(page, _userFilter), _nomeUser=_userFilter)


@User.route('/listCodUser')
@login_required
@admin_required
def listCodUser():
    ultimo_cod_user = Usuarios.query.order_by(Usuarios.codUser.desc()).first()
    if not ultimo_cod_user is None:
        partes = ultimo_cod_user.codUser.split("-")
        _ultimoNumero = int(partes[-1]) + 1
        novoCodUser = "127-USER-000" + str(_ultimoNumero)
    else:
        novoCodUser = "127-ADMIN-001"

    return render_template('criarUsuarios.html', novoCodUser=novoCodUser)


@User.route('/createUser', methods=['GET', 'POST'])
@login_required
@admin_required
def createUser():
    _coduser = request.form.get('codUser')
    _nome = request.form.get('nome')
    _cpf = request.form.get('cpf')
    _endereco = request.form.get('endereco')
    _contato = request.form.get('contato')
    _email = request.form.get('email')
    _senha = request.form.get('senha')
    _tipoBotao = request.form.get('bt1')
    partes = _coduser.split("-")
    _status = str(partes[1]).upper()
    if request.method == 'POST':
        if UserController.checkEmail(_email):
            flash('Email já cadastrado', 'error')
        else:
            if any((x is None or len(x) < 1) for x in [_coduser, _cpf, _nome, _endereco, _contato, _email, _senha, _status]):
                flash('Preencha todos os campos do formulário', 'error')
            else:
                if Regex.contatoRegex(_contato):
                    if Regex.emailRegex(_email):
                        if UserController.createUser(_coduser, _cpf, _nome, _endereco, _contato, _email, _senha, _status):
                            return redirect(url_for('router.user.listUser'))
                        else:
                            flash('CPF já cadastrado', 'error')
                    else:
                        flash('E-mail inválido', 'error')
                else:
                    flash('Celular inválido', 'error')

    ultimo_cod_user = Usuarios.query.order_by(Usuarios.codUser.desc()).first()
    if not ultimo_cod_user is None:
        partes = ultimo_cod_user.codUser.split("-")
        _ultimoNumero = int(partes[-1]) + 1
        novoCodUser = "127-USER-000" + str(_ultimoNumero)
    else:
        novoCodUser = "127-ADMIN-001"

    return render_template('criarUsuarios.html', novoCodUser=novoCodUser)


@User.route('/<int:id>/updateUser', methods=['GET', 'POST'])
@login_required
@admin_required
def updateUser(id):
    _user = Usuarios.query.filter_by(id=id).first()
    if request.method == 'POST':
        _cpf = request.form.get('cpf')
        _nome = request.form.get('nome')
        _endereco = request.form.get('endereco')
        _contato = request.form.get('contato')
        _email = request.form.get('email')
        if any((x is None or len(x) < 1) for x in [_cpf, _nome, _endereco, _contato, _email]):
            flash('Preencha todos os campos do formulário', 'error')
        else:
            if UserController.updateUser(id, _cpf, _user.codUser, _nome, _endereco, _contato, _email, _user.status):
                return redirect(url_for('router.user.listUser'))
            else:
                flash('Usuário já cadastrado', 'error')
    return render_template('atualizarUsuarios.html', user=_user)


@User.route('/<int:id>/removeUser', methods=['GET', 'POST'])
@login_required
@admin_required
def removeUser(id):
    UserController.removeUser(id)
    return redirect(url_for('router.user.listUser'))
