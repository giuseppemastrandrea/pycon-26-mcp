"""
Conference Buddy — Client MCP (singolo server).

Si connette al server MCP chuck e fa le chiamate esplicite alle primitive.

Requisiti:
    pip install mcp

Uso:
    python 02_mcp_client.py
"""

import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVERS_DIR = Path(__file__).parent / "servers"

server_params = StdioServerParameters(
    command="python",
    args=[str(SERVERS_DIR / "chuck.py")],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discovery
            tools = await session.list_tools()
            print("Tool disponibili:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description}")

            # Invocazione
            result = await session.call_tool("chuck_norris_joke", {})
            print(f"\nRisultato: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
