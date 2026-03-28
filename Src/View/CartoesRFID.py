from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required
from config import db, admin_required
from Src.Controller.Cartoes import CartoesController

bp_cadCartoes = Blueprint("cadCartao", __name__)


@bp_cadCartoes.route('cadastroCartao', methods=['POST'])
@login_required
@admin_required
def cadastroCartao():
    if request.method == 'POST':
        _idUser = request.form.get('bt1')
        _CadRFID = request.form.get('rfid')
        _codUser = request.form.get('codUser')
        if any((x is None or len(x) < 1) for x in [_CadRFID, _idUser]):
            flash('Preencha todos os campos do formulário', 'error')
        else:
            if CartoesController.createCartao(_CadRFID, _idUser):
                usuarios = CartoesController.ListCartoes()
                return render_template('listaUsuariosSemcartao.html', usuarios=usuarios)
            else:
                flash('Cartão RFID ou Usuário já cadastrado', 'error')
            return render_template('cadastroCartaoRFID.html', codUser=_codUser, idUser=_idUser)


@bp_cadCartoes.route('/atualizarCartao/<codigoUser>/<idUser>', methods=['GET'])
@login_required
@admin_required
def atualizarCartao(codigoUser, idUser):
    return render_template('cadastroCartaoRFID.html', codUser=codigoUser, idUser=idUser)


@bp_cadCartoes.route('/ListCartao', methods=['GET'])
@login_required
@admin_required
def ListCartao():
    # Chame a função CartoesController.ListCartoes() e passe o resultado para render_template
    usuarios = CartoesController.ListCartoes()
    return render_template('listaUsuariosSemcartao.html', usuarios=usuarios)


@bp_cadCartoes.route('/FiltrarUser', methods=['GET'])
@login_required
@admin_required
def FiltrarUser():
    _codUsuario = request.values.get('codUser')
    usuarios = CartoesController.FiltrarUsuarios(_codUsuario)
    return render_template('listaUsuariosSemcartao.html', usuarios=usuarios)
