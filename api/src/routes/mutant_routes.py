"""
Endpoints públicos relacionados a mutantes/estudantes para testes e
registro inicial. Contém utilitários de conexão e exemplares simples.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.mutantes_schema import MutanteCreate
from dependencies import get_session
from database import engine
from dependencies import get_session
from models import Mutante

mutant_router = APIRouter(prefix="/student", tags=["student"])


@mutant_router.get("/")
async def home():
    """
    Mensagem de boas-vindas simples para a rota raiz.
        
    Returns:
        dict: Mensagem de boas-vindas.
    """
    return {"msg": "Welcome, student!"}


@mutant_router.post("/register_mutant")
async def criar(
    mutant_schema: MutanteCreate
):
    """
    Recebe um objeto de criação de mutante e devolve-o (placeholder).
    
    Args:
        mutant_schema (MutanteCreate): Dados do mutante a ser criado.
        
    Returns:
        dict: O objeto de mutante recebido.
    """
    return {"msg": mutant_schema}

@mutant_router.get("/see_mutants")
async def seeAll(
    cursor = Depends(get_session)
):
    """
    Executa consulta direta para retornar todos os mutantes.
    
    Args:
        cursor: Conexão de banco de dados injetada pela dependência.
    
    Returns:
        dict: Lista de mutantes retornada pela consulta.
    """
    cursor.execute("select * from mutantes")
    resultado = cursor.fetchall()
    return {"msg": resultado}

@mutant_router.get("/try_connection")
async def get_connection_test(session: Session = Depends(get_session)):
    """
    Ponto de verificação para testar a conexão com o banco.
    
    Args:
        session (Session): Conexão de banco de dados injetada pela dependência.
        
    Returns:
        dict: Mensagem indicando sucesso ou falha da conexão.
    """
    # TODO verify if connection to database is working
    # session.query(Mutantes)

    print(session)


@mutant_router.get("/see_mutants")
async def see_mutants(
    id: int,
    session: Session = Depends(get_session)
):
    """
    Retorna um mutante específico pelo ID para teste de consulta.

    Args:
        id (int): ID do mutante a ser buscado.
        session (Session, optional): Conexão do banco de dados. Defaults to Depends(get_session).

    Returns:
        dict: Dados do mutante correspondente ao ID fornecido.
    """
    
    mutants = session.query(Mutante).filter(Mutante.id==id).first()

    return {"msg": mutants}


@mutant_router.get("/info")
async def get_mutante_info(
    id_mutante: int,
    session: Session = Depends(get_session)
):
    """
    Retorna informações básicas do mutante: nome, id e turma formatada.

    Args:
        id_mutante (int): ID do mutante.
        session (Session, optional): Conexão do banco de dados. Defaults to Depends(get_session).

    Raises:
        HTTPException: 404 se o mutante não for encontrado.

    Returns:
        MutanteInfoSchema: Nome, ID e turma do mutante.
    """
    from fastapi import HTTPException
    from schemas.mutantes_schema import MutanteInfoSchema

    mutante = session.query(Mutante).filter(Mutante.id == id_mutante).first()

    if not mutante:
        raise HTTPException(status_code=404, detail="Mutante não encontrado.")

    turma_str = ""
    if mutante.turma:
        turma_str = f"{mutante.turma.serie}° ANO {mutante.turma.turma}"

    return MutanteInfoSchema(
        id=mutante.id,
        nome=mutante.nome,
        turma=turma_str
    )


@mutant_router.get("/my_subjects")
async def get_mutante_subjects(
    id_mutante: int,
    session: Session = Depends(get_session)
):
    """
    Retorna todas as matérias em que o mutante está matriculado,
    incluindo o ID da matéria, nome e nome do professor.

    Args:
        id_mutante (int): ID do mutante.
        session (Session, optional): Conexão do banco de dados.

    Returns:
        List[MutanteMateriaInfoSchema]: Lista de matérias do aluno.
    """
    from fastapi import HTTPException
    from schemas.mutantes_schema import MutanteMateriaInfoSchema
    from models import MutantesMaterias

    registros = session.query(MutantesMaterias).filter(
        MutantesMaterias.mutante_id == id_mutante
    ).all()

    if not registros:
        raise HTTPException(status_code=404, detail="Nenhuma matéria encontrada para este aluno.")

    return [
        MutanteMateriaInfoSchema(
            materia_id=r.materias.id,
            materia=r.materias.nome,
            professor=r.materias.professor.nome
        )
        for r in registros
    ]