from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Esquema base para clientes com campos compartilhados."""

    nome: str
    telefone: str
    email: Optional[EmailStr] = None
    endereco: str
    complemento: Optional[str] = None
    bairro: str
    cep: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: bool = True


class ClienteCreate(ClienteBase):
    """Esquema para criação de clientes."""

    pass


class ClienteUpdate(BaseModel):
    """Esquema para atualização de clientes, todos os campos são opcionais."""

    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    """Esquema para resposta com dados de clientes."""

    id: int
    data_cadastro: datetime

    class Config:
        from_attributes = True  # Para permitir conversão de ORM para Pydantic

    # Alias para manter compatibilidade com a API
    @property
    def cliente_id(self) -> int:
        return self.id
