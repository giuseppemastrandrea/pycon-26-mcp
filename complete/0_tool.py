# -*- coding: utf-8 -*-

import os

import requests
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models.base import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from tools.search import search_talks, suggest_schedule, speaker_info

load_dotenv()

# GROQ_API_KEY = os.environ["GROQ_API_KEY"]


def show_messages(response):
    for msg in response["messages"]:
        print(f"--- {msg.type.upper()} ---")
        print(f"Contenuto: {msg.content or '(vuoto)'}")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"Tool calls: {msg.tool_calls}")
        print()


search_talks_tool = tool(search_talks)
suggest_schedule_tool = tool(suggest_schedule)
speaker_info_tool = tool(speaker_info)


@tool
def chuck_norris_joke() -> str:
    """Ottieni una barzelletta casuale su Chuck Norris.
    Usa questo tool quando l'utente chiede una barzelletta, un fatto divertente o qualcosa su Chuck Norris.
    """
    return requests.get("https://api.chucknorris.io/jokes/random").json().get("value")


config = {"configurable": {"thread_id": "chat-1"}}

model = init_chat_model(model="groq:llama-3.3-70b-versatile", temperature=0)

agent = create_agent(
    model=model,
    tools=[chuck_norris_joke]
    + [search_talks_tool, suggest_schedule_tool, speaker_info_tool],
    system_prompt=(
        "Sei Conference Buddy, un assistente per la PyCon Italia 2026 a Bologna "
        "(27-30 maggio). Aiuti le persone a trovare talk, suggerisci percorsi "
        "e dai info sugli speaker. Rispondi SEMPRE in italiano. Quando hai una risposta in inglese da un tool, traducilo SEMPRE in italiano."
        "Quando un tool ti restituisce un contenuto (una barzelletta, un risultato di ricerca, ecc.), includilo sempre nella tua risposta all'utente."
    ),
    checkpointer=InMemorySaver(),
)


def main():
    print("=" * 60)
    print("  🎤 Conference Buddy — PyCon Italia 2026")
    print("  (versione SENZA MCP — tool accoppiato)")
    print("=" * 60)
    print("Chiedimi qualcosa sul programma! (quit per uscire)\n")

    while True:
        user_input = input("Tu: ").strip()

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Alla prossima! 👋")
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, config=config
        )

        # Mostriamo le chiamate a tool, poi solo la risposta finale
        # show_messages(result)
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  🔧 Tool call: {tc['name']}({tc['args']})")
            if msg.type == "tool":
                print(f"  📦 Tool result: {msg.content[:200]}...")

        print(f"\n🤖: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
