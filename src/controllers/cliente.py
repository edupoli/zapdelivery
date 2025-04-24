from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from prisma import Prisma
from database import get_db
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from services.cliente import ClienteService

router = APIRouter()


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_client(cliente: ClienteCreate, prisma: Prisma = Depends(get_db)):
    """Cria um novo cliente."""
    return await ClienteService.create_client(prisma, cliente)


@router.get("/", response_model=List[ClienteResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = None,
    prisma: Prisma = Depends(get_db),
):
    """Lista todos os clientes com opção de filtrar por status ativo."""
    return await ClienteService.list_clients(prisma, skip, limit, ativo)


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_client_by_id(cliente_id: int, prisma: Prisma = Depends(get_db)):
    """Obtém um cliente pelo ID."""
    return await ClienteService.get_client_by_id(prisma, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update_client(
    cliente_id: int, cliente: ClienteUpdate, prisma: Prisma = Depends(get_db)
):
    """Atualiza um cliente existente."""
    return await ClienteService.update_client(prisma, cliente_id, cliente)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(cliente_id: int, prisma: Prisma = Depends(get_db)):
    """Remove um cliente pelo ID."""
    await ClienteService.delete_client(prisma, cliente_id)
    return None


@router.patch("/{cliente_id}/ativar", response_model=ClienteResponse)
async def activate_client(cliente_id: int, prisma: Prisma = Depends(get_db)):
    """Ativa um cliente pelo ID."""
    return await ClienteService.activate_client(prisma, cliente_id)


@router.patch("/{cliente_id}/desativar", response_model=ClienteResponse)
async def deactivate_client(cliente_id: int, prisma: Prisma = Depends(get_db)):
    """Desativa um cliente pelo ID."""
    return await ClienteService.deactivate_client(prisma, cliente_id)


@router.get("/busca/", response_model=List[ClienteResponse])
async def search_clients(
    termo: str = Query(..., min_length=1), prisma: Prisma = Depends(get_db)
):
    """Busca clientes por nome, email ou telefone."""
    return await ClienteService.search_clients(prisma, termo)
