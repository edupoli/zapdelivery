import asyncio
from mcp_use import MCPClient, MCPAgent
from langchain_groq import ChatGroq
from pathlib import Path


async def main():
    # Create client with multiple servers
    # Obter o diretório do script atual
    script_dir = Path(__file__).parent

    # Caminho completo para o arquivo JSON
    config_path = script_dir / "mcp-servers.json"

    # Verifique se o arquivo existe
    if not config_path.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado em: {config_path}"
        )

    # Create client with multiple servers
    client = MCPClient.from_config_file(str(config_path))

    # Create agent with the client
    agent = MCPAgent(
        llm=ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct"),
        client=client,
        use_server_manager=True,  # Enable the Server Manager
    )

    try:
        # Run a query that uses tools from multiple servers
        result = await agent.run(
            "Search for a nice place to stay in Barcelona on Airbnb, "
            "then use Google to find nearby restaurants and attractions."
        )
        print(result)
    finally:
        # Clean up all sessions
        await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())
