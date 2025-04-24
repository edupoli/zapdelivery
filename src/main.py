from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from controllers.cliente import router as cliente_router
from fastapi_mcp import FastApiMCP
from datetime import datetime

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="Hachiban Delivery API",
    version="1.0.0",
    description="API para sistema de delivery Hachiban",
    contact={"name": "Equipe Hachiban", "email": "contato@hachiban.com.br"},
    license_info={"name": "MIT"},
)


@app.get("/health")
async def health_check():
    try:
        # Verificação simples de saúde
        return {"status": "ok", "timestamp": datetime.now().isoformat()}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Serviço indisponível",
            headers={"WWW-Authenticate": "Basic"},
        )


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registra os routers
app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])

# Mount the MCP server directly to your FastAPI app
mcp = FastApiMCP(app)
mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
