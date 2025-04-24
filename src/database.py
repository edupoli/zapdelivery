from prisma import Prisma
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


# Contexto assíncrono para gerenciar a conexão com o banco de dados
@asynccontextmanager
async def get_prisma():
    prisma = Prisma()
    try:
        await prisma.connect()
        yield prisma
    finally:
        await prisma.disconnect()


# Função para obter uma instância do cliente Prisma para uso com Depends
async def get_db():
    async with get_prisma() as prisma:
        yield prisma
