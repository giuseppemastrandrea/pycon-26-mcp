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
    client = MultiServerMCPClient({})

    # model = init_chat_model("groq:llama-3.3-70b-versatile", temperature=0)

    while True:
        user_input = input("Tu: ").strip()

        """
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  🔧 Tool call: {tc['name']}({tc['args']})")
            if msg.type == "tool":
                print(f"  📦 Tool result: {msg.content[:200]}...")

        print(f"\n🤖: {result['messages'][-1].content}\n")
        """


if __name__ == "__main__":
    asyncio.run(main())
