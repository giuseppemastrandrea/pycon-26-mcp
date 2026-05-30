"""
Conference Buddy — Agente esposto come Tool MCP (composizione vera).

L'agente si connette al server MCP pycon come CLIENT,
scopre i tool via protocollo, e poi si espone a sua volta
come SERVER MCP con un unico tool: ask_conference_buddy.

È composizione MCP end-to-end:
  Client esterno → [agent_as_tool] → [pycon server] → tool

Test con Inspector:
    mcp dev servers/agent_as_tool.py
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVERS_DIR = Path(__file__).parent


# Agent e client inizializzati al primo uso
_agent = None
_client = None


async def get_agent():
    pass


@mcp.tool()
async def ask_conference_buddy(question: str) -> str:
    """Fai una domanda al Conference Buddy sulla PyCon Italia 2026.

    L'agente cercherà nel programma, consulterà le info sugli speaker,
    e ti darà una risposta ragionata.

    Args:
        question: La tua domanda sulla conferenza (es. "Quali talk su ML ci sono giovedì?").
    """
    pass


if __name__ == "__main__":
    pass
    # mcp.run(transport="stdio")
