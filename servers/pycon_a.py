"""
Conference Buddy — Server MCP (solo tool per ora).

Log su /tmp/mcp_pycon.log per debug quando gira sotto Claude Desktop.
"""

import logging
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    filename="/tmp/mcp_pycon.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("pycon")

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.search import search_talks, suggest_schedule, speaker_info

mcp = FastMCP("Conference Buddy")

# registra le funzioni come tool fastmcp


if __name__ == "__main__":
    log.info("Server pycon avviato")
    mcp.run(transport="stdio")
