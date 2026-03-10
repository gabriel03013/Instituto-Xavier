"""
Rotas relacionadas aos mutantes, abrangendo cadastro inicial, listagem,
consulta, finalização de registro e consulta de notas pessoais.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import List
from dao.mutante_dao import MutanteDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.turmas_dao import TurmasDAO
from schemas.mutantes_schema import MutanteBase, MutanteUpdate, MutanteInfoSchema, MutanteMateriaInfoSchema, ResetPasswordSchema
from schemas.mutantes_materias_schema import MyGradeSchema
from dependencies import get_session
from database import engine
from models import Mutante, MutantesMaterias
from services.mutante_service import MutanteService
from dao.boletim_dao import BoletimDAO


mutante_router = APIRouter(prefix="/mutant", tags=["mutant"])


def get_mutante_service(session: Session = Depends(get_session)) -> MutanteService:
    """
    Cria instância do serviço de mutantes.
    
    Args:
        session (Session): Conexão do banco de dados injetada pela dependência.
    
    Returns:
        MutanteService: Instância do serviço de mutantes.
    """
    return MutanteService(
        mutante_dao=MutanteDAO(session),
        turmas_dao=TurmasDAO(session),
        mutantes_materias_dao=MutantesMateriasDAO(session)
    )

@mutante_router.get("/")
async def home():
    """
    Endpoint de boas-vindas para mutantes.
    
    Returns:
        dict: Mensagem de boas-vindas.
    """
    return {"msg": "Welcome, mutant!"}


# -- CREATE --
@mutante_router.post("/register_mutante")
async def register_mutante(
    mutante_schema: MutanteBase,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Registra um novo mutante no sistema.
    
    A matrícula é validada previamente - o administrador já inseriu o número no banco de dados.
    Este endpoint verifica se a matrícula existe e cria o registro do mutante.
    
    Args:
        mutante_schema (MutanteBase): Schema com os dados iniciais do mutante.
        session (Session, optional): Conexão do banco de dados injetada pela dependência.
        service (MutanteService, optional): Service para lógica e validação. Defaults to Depends(get_mutante_service).
    
    Returns:
        dict: Mensagem de sucesso com o ID do novo mutante.
    """
    new_mutante = service.registrar_novo_mutante(mutante_schema)

    return {"msg": f"New Mutante inserted successfuly! ID: {new_mutante.id}"}


# -- READ --
@mutante_router.get("/list")
async def list_mutantes(
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Lista todos os mutantes registrados no sistema.
    
    Args:
        service (MutanteService, optional): Service para lógica e validação. Defaults to Depends(get_mutante_service).
    
    Raises:
        HTTPException: Levanta 404 se nenhum mutante for encontrado.
    
    Returns:
        dict: Dicionário contendo lista de todos os mutantes.
    """
    mutantes = service.listar_mutantes()

    if not mutantes:
        raise HTTPException(status_code=404, detail="Couldn't find any mutante")

    return {"mutantes": mutantes}


@mutante_router.get("/find_mutante")
async def find_mutante(
    id: int,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Busca um mutante específico pelo ID fornecido.
    
    Args:
        id (int): ID do mutante a ser buscado.
        service (MutanteService, optional): Service para lógica e validação. Defaults to Depends(get_mutante_service).
    
    Returns:
        dict: Dicionário contendo os dados do mutante encontrado.
    """
    
    return {"mutante": "mutante"}


@mutante_router.put("/complete_registration")
async def complete_registration(
    mutante_schema: MutanteUpdate,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Completa o registro de um mutante já cadastrado.
    
    O mutante fornece o número da matrícula e o back-end verifica se ela existe e pode ser usada,
    atualizando o registro com os dados adicionais fornecidos nessa requisição.
    
    Args:
        mutante_schema (MutanteUpdate): Schema com os dados a serem atualizados.
        service (MutanteService, optional): Service para lógica e validação. Defaults to Depends(get_mutante_service).
    
    Raises:
        HTTPException: Caso a matrícula não exista ou haja erro na validação.
    
    Returns:
        dict: Mensagem de sucesso confirmando o registro atualizado.
    """
    try:
        service.completar_cadastro(mutante_schema)

        return {"msg": "Registration completed successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@mutante_router.put("/reset_password")
async def reset_password(
    dados: ResetPasswordSchema,
    service: MutanteService = Depends(get_mutante_service)
):
    try:    
        service.redefinir_senha(
            chave_seguranca=dados.chave_seguranca,
            nova_senha=dados.nova_senha
        )

        return {"msg": "Password changed successfully!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@mutante_router.patch("/{id_mutante}")
async def update_mutante(
    id_mutante: int,
    mutante_schema: MutanteUpdate,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Atualiza um mutante existente.
    """
    try:
        return service.atualizar_mutante(id_mutante, mutante_schema)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@mutante_router.get("/my_grades", response_model=List[MyGradeSchema])

async def see_my_grades(
    id_mutante: int,
    session: Session = Depends(get_session)
):
    """
    Recupera as notas pessoais do mutante.
    
    Args:
        id_mutante (int): ID do mutante para o qual buscar as notas.
        session (Session, optional): Conexão do banco de dados injetada pela dependência. Defaults to Depends(get_session).
    
    Raises:
        HTTPException: Levanta 404 se nenhuma nota for encontrada.
    
    Returns:
        dict: Dicionário contendo o boletim de notas do mutante.
    """
    boletim_dao = BoletimDAO(session)
    boletim = boletim_dao.obter_minhas_notas(id_mutante)

    if not boletim:
        raise HTTPException(status_code=404, detail="Grades are not available.")
    
    return [MyGradeSchema.model_validate(dict(row)) for row in boletim]


@mutante_router.get("/info")
async def get_mutante_info(
    id_mutante: int,
    session: Session = Depends(get_session)
):
    """
    Retorna informações básicas do mutante: nome, id e turma formatada.

    Args:
        id_mutante (int): ID do mutante.
        session (Session, optional): Conexão do banco de dados.

    Raises:
        HTTPException: 404 se o mutante não for encontrado.

    Returns:
        MutanteInfoSchema: Nome, ID e turma do mutante.
    """
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


@mutante_router.get("/my_subjects")
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
    registros = session.query(MutantesMaterias).filter(
        MutantesMaterias.mutante_id == id_mutante
    ).all()

    return [
        MutanteMateriaInfoSchema(
            materia_id=r.materias.id,
            materia=r.materias.nome,
            professor=r.materias.professor.nome if r.materias.professor else "Sem professor"
        )
        for r in registros if r.materias
    ]


@mutante_router.delete("/{id_mutante}")
async def delete_mutante(
    id_mutante: int,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Deleta um mutante do sistema.
    
    Args:
        id_mutante (int): ID do mutante a ser deletado.
        service (MutanteService): Service para lógica e validação.
    
    Returns:
        dict: Mensagem de sucesso.
    """
    try:
        service.deletar_mutante(id_mutante)
        return {"msg": "Mutante deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))