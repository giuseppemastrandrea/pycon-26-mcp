"""
Conference Buddy — Server MCP (solo tool per ora).

Log su /tmp/mcp_pycon.log per debug quando gira sotto Claude Desktop.
"""

import json
import logging
import os

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

port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("Conference Buddy", host="0.0.0.0", port=port)


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


# ===========================================================================
# PROMPTS (user-controlled)
# ===========================================================================


@mcp.prompt()
def recommend_talks(interests: str, level: str = "any") -> str:
    """Chiedi consigli personalizzati sui talk da seguire.

    Args:
        interests: I tuoi interessi (es. "machine learning, API, testing").
        level: Il tuo livello: "Beginner", "Intermediate", "Advanced", o "any" per tutti.
    """
    level_filter = f"\nFiltra per livello: {level}." if level != "any" else ""
    return (
        f"Sei Conference Buddy, assistente per la PyCon Italia 2026 a Bologna (27-30 maggio).\n\n"
        f"L'utente è interessato a: {interests}.{level_filter}\n\n"
        f"Usa il tool search_talks per trovare talk rilevanti, poi suggerisci un percorso "
        f"personalizzato. Per ogni talk consigliato spiega brevemente perché è adatto. "
        f"Considera le sovrapposizioni di orario e suggerisci alternative se necessario. "
        f"Rispondi in italiano."
    )


if __name__ == "__main__":
    import os
    import sys

    log.info("Server pycon avviato")
    transport = "stdio"
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]

    if transport == "http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport=transport)
