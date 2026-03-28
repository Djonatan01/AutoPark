from flask import Blueprint, render_template,request,flash
from flask_login import login_required
from Src.Controller.Vagas import ControleVagas
from Src.Model.BancoDados import Vagas
import json
from pytz import timezone
from datetime import datetime, timedelta

vaga = Blueprint('vagas', __name__)


@vaga.route('/Cadastrar')
def Cadastrar():

  ultimaVaga = Vagas.query.order_by(Vagas.idVaga.desc()).first()

  if ultimaVaga is None:
    ultimaVaga = 0
  else:
    ultimaVaga = ultimaVaga.nVaga.split("-")
    ultimaVaga = int(ultimaVaga[0])

    CountVagas, descricaoVagas,idVagas,totalVagasAcess = ControleVagas.ConsultaTotalVagas()
    # Cálculo da porcentagem
    porcentagemAcessibilidade = (totalVagasAcess / CountVagas) * 100

    if porcentagemAcessibilidade < 0.07:

      flash(f'A lei Lei Federal nº 13.146/2015 e Lei Federal nº 10.741/2003 informa que deve ser reservado 7% das vagas para idosos e pessoas com necessidades especiais {porcentagemAcessibilidade} % ', 'error')

  return render_template('cadastrarVagas.html',ultimaVaga = ultimaVaga + 1)

@vaga.route('/cadastro',methods = ['POST'])
def cadastro():
  if request.method == 'POST':
    _NumVaga = request.form.get('NumVaga')
    _TipoVaga = request.form.get('TipoVaga')
    if _NumVaga != "" and _TipoVaga != "" :
      ControleVagas.CadastroVaga(_NumVaga,_TipoVaga)
    else:
      flash("Todos os campos devem estar preenchidos",'error')

    ultimaVaga = Vagas.query.order_by(Vagas.idVaga.desc()).first()
    if not ultimaVaga is None:
      ultimaVaga = ultimaVaga.nVaga.split("-")
      ultimaVaga = int(ultimaVaga[0])
    else:
      ultimaVaga = 0
      
    CountVagas, descricaoVagas,idVagas,totalVagasAcess = ControleVagas.ConsultaTotalVagas()
    # Cálculo da porcentagem
    porcentagemAcessibilidade = (totalVagasAcess / CountVagas) * 100

    if porcentagemAcessibilidade < 0.07:
      flash(f'A lei Lei Federal nº 13.146/2015 e Lei Federal nº 10.741/2003 informa que deve ser reservado 7% das vagas para idosos e pessoasl com necessidades especiais {porcentagemAcessibilidade} % ', 'error')

    return render_template('cadastrarVagas.html',ultimaVaga = ultimaVaga + 1)

@vaga.route('/consultaVagas')
@login_required
def consultaVagas():

  CountVagas, descricaoVagas,idVagas,totalVagasAcess = ControleVagas.ConsultaTotalVagas()

  novaLista = json.dumps(descricaoVagas)

  statusVagas = ControleVagas.consultarStatusVaga()

  statusVagas = json.dumps(statusVagas)

  return render_template('reserve.html', CountVagas = CountVagas, descricaoVagas=novaLista,idVagas=idVagas, statusVagas=statusVagas)

@vaga.route('/reserva', methods=['POST'])
@login_required
def reserva():

  data = request.get_json()

  vaga_id = data.get('vagaId')
  user_id = data.get('userId')

  sao_paulo = timezone("America/Sao_Paulo")
  now = datetime.now(sao_paulo)
  # Adicionando 30 minutos
  new_time = now + timedelta(minutes=30)
  # Formatando a data e a hora
  data_hora = new_time.strftime("%d/%m/%Y %H:%M:%S")

  # status da vaga L = Livre, O = Ocupada, R = Reservada
  ControleVagas.atualizaStatusVaga(vaga_id,user_id,'','',data_hora,'R')

  return render_template('index.html')