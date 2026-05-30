FROM python:3.12-slim

WORKDIR /app

COPY data/ data/
COPY tools/ tools/
COPY servers/pycon_gamma.py server.py

RUN pip install "mcp[cli]"

EXPOSE 8000

CMD ["python", "server.py", "--transport", "http"]