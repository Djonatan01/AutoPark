from Src.Model.BancoDados import Registro, CartaoRFID, Usuarios,situacaoVagas
from Src.Controller.Vagas import ControleVagas
from datetime import datetime
from pytz import timezone
from config import db
from sqlalchemy.sql import and_

class RFID:
    def Register(rfidCode):
        # Filter user (Unique register)
        rfid = CartaoRFID.query.filter_by(numRfid=rfidCode).first()
        if rfid == None:
            print("Não existe cadastro")
            return "Não registrado"
        else:
            # Grab date/time
            sao_paulo = timezone("America/Sao_Paulo")
            now = datetime.now(sao_paulo)
            data = now.strftime("%d/%m/%Y")
            hora = now.strftime("%H:%M:%S")
            # Filter rfid regiters
            query = Registro.query.filter_by(rfid=rfidCode, dt=data).all()
            status = ( "Saída" if query != [] and query[-1].statusReg == "Entrada" else "Entrada")
            # rfid.id é referente ao ID do usuário que esta atribuido o cartão RFID
            rfid.id
            # Verificar se o usuário tem uma vaga reservada
            UserVaga = db.session.query(situacaoVagas).filter(and_ (situacaoVagas.idUser == rfid.id, situacaoVagas.status!= "P")).first()

            if UserVaga != None:
                data_hora = data + " " +  hora
                if status == "Saída":
                    ControleVagas.atualizaStatusVaga(UserVaga.idVaga,UserVaga.idUser,'',data_hora,'','P')
                else:
                    ControleVagas.atualizaStatusVaga(UserVaga.idVaga,UserVaga.idUser,data_hora,'','','O')

            # Create an obj of Register and add in DB
            reg = Registro(rfid.id, rfidCode, data, hora, status)
            db.session.add(reg)
            db.session.commit()
            return "Registrado"

    def List(page, _data, per_page=5):
        sao_paulo = timezone("America/Sao_Paulo")
        now = datetime.now(sao_paulo)
        data = now.strftime("%d/%m/%Y")
        if _data == "None" or _data is None or len(_data) < 1:
            query = (
                Registro.query.join(Usuarios, Registro.id == Usuarios.id)
                .add_columns(Usuarios.nome, Registro.dt, Registro.hr, Registro.statusReg)
                .filter(Registro.dt == data)
                .paginate(page=page, per_page=per_page)
            )
        else:
            _dataFilter = datetime.strptime(
                _data, "%Y-%m-%d").strftime("%d/%m/%Y")
            query = (
                Registro.query.join(Usuarios, Registro.id == Usuarios.id)
                .add_columns(Usuarios.nome, Registro.dt, Registro.hr, Registro.statusReg)
                .filter(Registro.dt == _dataFilter)
                .paginate(page=page, per_page=per_page)
            )
        queryCount = Registro.query.count()
        return {
            "registros": query,
            "page": page,
            "per_page": per_page,
            "count": queryCount,
        }
