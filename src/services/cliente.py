from prisma import Prisma
from fastapi import HTTPException
from typing import Optional, Dict, Any
from schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    """Service for managing CRUD operations for Clients."""

    @staticmethod
    async def create_client(prisma: Prisma, client_data: ClienteCreate):
        """Creates a new client in the database."""
        try:
            new_client = await prisma.cliente.create(data=client_data.dict())
            return new_client
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error creating client: {str(e)}"
            )

    @staticmethod
    async def list_clients(
        prisma: Prisma, skip: int = 0, limit: int = 100, active: Optional[bool] = None
    ):
        """Lists clients with optional active status filter."""
        try:
            where: Dict[str, Any] = {}
            if active is not None:
                where["ativo"] = active

            clients = await prisma.cliente.find_many(
                skip=skip, take=limit, where=where, order={"id": "asc"}
            )
            return clients
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error listing clients: {str(e)}"
            )

    @staticmethod
    async def get_client_by_id(prisma: Prisma, client_id: int):
        """Gets a client by ID."""
        try:
            client = await prisma.cliente.find_unique(where={"id": client_id})
            if client is None:
                raise HTTPException(status_code=404, detail="Client not found")
            return client
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error fetching client: {str(e)}"
            )

    @staticmethod
    async def update_client(prisma: Prisma, client_id: int, client_data: ClienteUpdate):
        """Updates an existing client."""
        try:
            # Verify client exists
            await ClienteService.get_client_by_id(prisma, client_id)

            # Filter non-None fields
            update_data = {k: v for k, v in client_data.dict().items() if v is not None}

            # Update the client
            updated_client = await prisma.cliente.update(
                where={"id": client_id}, data=update_data
            )
            return updated_client
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error updating client: {str(e)}"
            )

    @staticmethod
    async def delete_client(prisma: Prisma, client_id: int):
        """Deletes a client by ID."""
        try:
            # Verify client exists
            await ClienteService.get_client_by_id(prisma, client_id)

            # Delete the client
            await prisma.cliente.delete(where={"id": client_id})
            return None
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error deleting client: {str(e)}"
            )

    @staticmethod
    async def activate_client(prisma: Prisma, client_id: int):
        """Activates a client by ID."""
        try:
            # Verify client exists
            await ClienteService.get_client_by_id(prisma, client_id)

            # Activate client
            updated_client = await prisma.cliente.update(
                where={"id": client_id}, data={"ativo": True}
            )
            return updated_client
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error activating client: {str(e)}"
            )

    @staticmethod
    async def deactivate_client(prisma: Prisma, client_id: int):
        """Deactivates a client by ID."""
        try:
            # Verify client exists
            await ClienteService.get_client_by_id(prisma, client_id)

            # Deactivate client
            updated_client = await prisma.cliente.update(
                where={"id": client_id}, data={"ativo": False}
            )
            return updated_client
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error deactivating client: {str(e)}"
            )

    @staticmethod
    async def search_clients(prisma: Prisma, term: str):
        """Searches clients by name, email or phone."""
        try:
            clients = await prisma.cliente.find_many(
                where={
                    "OR": [
                        {"nome": {"contains": term, "mode": "insensitive"}},
                        {"email": {"contains": term, "mode": "insensitive"}},
                        {"telefone": {"contains": term, "mode": "insensitive"}},
                    ]
                }
            )
            return clients
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error searching clients: {str(e)}"
            )
