"""
Conference Buddy — Agente MCP.

Si connette ai server MCP e crea un agente con LLM.
Stessi server di Claude Desktop, ma con il modello che scegli tu.

Requisiti:
    pip install langchain-mcp-adapters langchain langgraph

Uso:
    python 02_mcp_client_multiserver.py
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

SERVERS_DIR = Path(__file__).parent / "servers"


async def main():
    client = MultiServerMCPClient(
        {
            "chuck": {
                "command": "python",
                "args": [str(SERVERS_DIR / "chuck.py")],
                "transport": "stdio",
            },
            "pycon": {
                "command": "python",
                "args": [str(SERVERS_DIR / "pycon_beta.py")],
                "transport": "stdio",
            },
        }
    )

    tools = await client.get_tools()
    print(f"Tool disponibili: {[t.name for t in tools]}\n")

    # model = init_chat_model("groq:llama-3.3-70b-versatile", temperature=0)
    model = init_chat_model("ollama:gemma4", temperature=0)

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "Sei Conference Buddy, un assistente per la PyCon Italia 2026 a Bologna "
            "(27-30 maggio). Aiuti le persone a trovare talk, suggerisci percorsi "
            "e dai info sugli speaker. Rispondi SEMPRE in italiano. "
            "Quando un tool ti restituisce un contenuto, includilo sempre nella tua risposta."
        ),
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": "chat-1"}}

    print("=" * 60)
    print("  🎤 Conference Buddy — PyCon Italia 2026")
    print("  (versione MCP — tool da server esterni)")
    print("=" * 60)
    print("Chiedimi qualcosa sul programma! (quit per uscire)\n")

    while True:
        user_input = input("Tu: ").strip()

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Alla prossima! 👋")
            break

        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  🔧 Tool call: {tc['name']}({tc['args']})")
            if msg.type == "tool":
                print(f"  📦 Tool result: {msg.content[:200]}...")

        print(f"\n🤖: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    asyncio.run(main())
