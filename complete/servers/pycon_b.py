"""
Conference Buddy — Server MCP (solo tool per ora).

Log su /tmp/mcp_pycon.log per debug quando gira sotto Claude Desktop.
"""

import json
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

from tools.search import search_talks, suggest_schedule, speaker_info, SCHEDULE

mcp = FastMCP("Conference Buddy")


# ===========================================================================
# TOOLS (model-controlled)
# ===========================================================================
mcp.tool()(search_talks)
mcp.tool()(suggest_schedule)
mcp.tool()(speaker_info)


# ===========================================================================
# RESOURCES (application-controlled, read-only)
# ===========================================================================


@mcp.resource("conference://tags")
def get_tags() -> str:
    """Lista di tutti i tag/argomenti disponibili nel programma della PyCon Italia 2026."""
    all_tags = sorted({tag for event in SCHEDULE for tag in event.get("tags", [])})
    return json.dumps(all_tags, indent=2, ensure_ascii=False)


DATA_DIR = Path(__file__).parent.parent / "data"
FAQ_PATH = DATA_DIR / "faq.md"


@mcp.resource("conference://faq")
def get_faq() -> str:
    """Domande frequenti sulla PyCon Italia 2026 (dal sito ufficiale)."""
    return FAQ_PATH.read_text(encoding="utf-8")


if __name__ == "__main__":
    log.info("Server pycon avviato")
    mcp.run(transport="stdio")
