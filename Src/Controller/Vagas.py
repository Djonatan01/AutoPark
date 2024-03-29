from Src.Model.BancoDados import situacaoVagas,Vagas
from config import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased

class ControleVagas():
    def ConsultaTotalVagas():
        ContVaga = Vagas.query.count()

        return ContVaga
    
    def CadastroVaga(numVaga,tipoVaga):
        
        novaVaga = Vagas(numVaga,tipoVaga.upper())
        db.session.add(novaVaga)
        try:
            db.session.commit()
            return True
        except IntegrityError:
            return False