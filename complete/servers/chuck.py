"""
Server MCP minimale — Chuck Norris jokes.

Log su /tmp/mcp_chuck.log per debug quando gira sotto Claude Desktop.
"""

import logging

import requests
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    filename="/tmp/mcp_chuck.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("chuck")

mcp = FastMCP("Chuck Norris")


@mcp.tool()
def chuck_norris_joke() -> str:
    """Ottieni una barzelletta casuale su Chuck Norris.
    Usa questo tool quando l'utente chiede una barzelletta, un fatto divertente o qualcosa su Chuck Norris.
    """
    log.info("chuck_norris_joke chiamato")
    joke = requests.get("https://api.chucknorris.io/jokes/random").json().get("value")
    log.info(f"joke ottenuto: {joke[:80]}...")
    return joke


if __name__ == "__main__":
    log.info("Server chuck avviato")
    mcp.run(transport="stdio")
