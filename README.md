# Interoperable Agents with MCP — Conference Buddy

Workshop pratico su **MCP (Model Context Protocol)** a cura di **Data Masters** per
**PyCon Italia 2026** (Bologna, 27–30 maggio). Costruiamo passo dopo passo **Conference Buddy**,
un assistente per la conferenza, partendo da un agente con tool "accoppiati" fino ad arrivare a
server MCP interoperabili e alla composizione di agenti.

L'idea di fondo: la stessa logica di business (cercare talk, suggerire un percorso, info sugli
speaker) può essere esposta in modi diversi. MCP la rende **interoperabile** — usabile da Claude
Desktop, da un agente LangGraph o da un altro server MCP, senza riscrivere nulla.

---

## Il percorso

Gli esercizi sono numerati e progressivi. I file alla radice e in `servers/` contengono gli
**scheletri da completare**; le soluzioni complete sono nella cartella [`complete/`](./complete).

| Step | File | Cosa si impara |
|------|------|----------------|
| 0 | [`0_tool.py`](./0_tool.py) | Agente LangGraph con tool **accoppiati** al codice (senza MCP). Il punto di partenza. |
| 1 | [`1_mcp_client_monoserver.py`](./1_mcp_client_monoserver.py) | Un **client MCP** che si connette a un singolo server via stdio e ne chiama le primitive. |
| 2 | [`2_mcp_client_multiserver.py`](./2_mcp_client_multiserver.py) | Un agente collegato a **più server MCP** insieme, con `MultiServerMCPClient`. |

### Server MCP da costruire (`servers/`)

| File | Focus |
|------|-------|
| [`chuck.py`](./servers/chuck.py) | Server MCP minimale: un solo **tool**. |
| [`pycon_a.py`](./servers/pycon_a.py) | Esponi la logica di `tools/search.py` come **tool** MCP. |
| [`pycon_b.py`](./servers/pycon_b.py) | Aggiungi le **resources** (dati read-only, application-controlled). |
| [`pycon_c.py`](./servers/pycon_c.py) | Aggiungi i **prompts** (template user-controlled). |
| [`pycon_d.py`](./servers/pycon_d.py) | **Agent-as-tool**: un agente che è client di un server MCP e a sua volta si espone come server MCP. Composizione end-to-end. |
| [`meteo.py`](./servers/meteo.py) | Esercizio libero: server meteo con le API Open-Meteo (geocoding + forecast, senza API key). |

---

## Struttura del repository

```
.
├── 0_tool.py                      # Step 0 — agente con tool accoppiati
├── 1_mcp_client_monoserver.py     # Step 1 — client MCP mono-server
├── 2_mcp_client_multiserver.py    # Step 2 — client MCP multi-server
├── servers/                       # Server MCP da completare (chuck, pycon_a..d, meteo)
├── tools/
│   └── search.py                  # Logica di business pura (riusata ovunque)
├── data/
│   ├── schedule.json              # Programma PyCon 2026 (157 eventi)
│   └── faq.md                     # FAQ della conferenza
├── complete/                      # Soluzioni complete di tutti gli step
├── slides/                        # Slide del workshop (Marp)
├── Dockerfile                     # Esponi un server MCP via HTTP in un container
├── requirements.txt
└── .env.example
```

`tools/search.py` è il cuore "neutro": funzioni pure senza decoratori né dipendenze da framework.
Lo stesso modulo viene riusato dallo step 0, dai server MCP e dalle soluzioni — è proprio questo il
punto del workshop.

---

## Setup

Requisiti: **Python 3.12+**.

```bash
# 1. Ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate

# 2. Dipendenze
pip install -r requirements.txt

# 3. Variabili d'ambiente
cp .env.example .env
# poi apri .env e inserisci la tua GROQ_API_KEY
```

La `GROQ_API_KEY` si ottiene gratuitamente su <https://console.groq.com>. Il file `.env` **non va
mai committato** (è già in `.gitignore`).

---

## Come si esegue

**Agente da terminale** (step 0, 1, 2) — chat interattiva:

```bash
python 0_tool.py
python 2_mcp_client_multiserver.py
```

**Testare un server MCP con l'Inspector** (UI di debug per tool/resources/prompts):

```bash
mcp dev servers/pycon_a.py
mcp dev servers/meteo.py
```

**Usare i server con Claude Desktop** — aggiungi al `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "conference-buddy": {
      "command": "python",
      "args": ["/percorso/assoluto/servers/pycon_c.py"]
    }
  }
}
```

> I server scrivono log di debug in `/tmp/mcp_*.log`: utili quando girano "in silenzio" dentro
> Claude Desktop.

**Esporre un server via HTTP** (Docker):

```bash
docker build -t conference-buddy .
docker run -p 8000:8000 conference-buddy
```

---

## Slide

Le slide sono in [`slides/slides.md`](./slides/slides.md) (formato [Marp](https://marp.app/)). Per
visualizzarle apri `slides/slides.html`, oppure rigenera con:

```bash
npx @marp-team/marp-cli slides/slides.md -o slides/slides.html
```

---

## Risorse

- **Specifica MCP**: <https://modelcontextprotocol.io>
- **Python SDK** (`mcp`): <https://github.com/modelcontextprotocol/python-sdk>
- **langchain-mcp-adapters**: <https://github.com/langchain-ai/langchain-mcp-adapters>
- **PyCon Italia 2026**: <https://pycon.it>
