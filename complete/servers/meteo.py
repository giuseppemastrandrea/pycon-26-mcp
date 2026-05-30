"""
Server MCP Meteo — Esercizio.

Usa Open-Meteo API (gratis, no API key):
- Geocoding: https://geocoding-api.open-meteo.com/v1/search?name={city}
- Forecast: https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true

Completa le funzioni!

Test:
    mcp dev servers/meteo.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Meteo")


@mcp.tool()
def geocode(city: str) -> str:
    """Cerca le coordinate geografiche di una città.

    Args:
        city: Nome della città (es. "Bologna", "Roma", "New York").
    """
    pass


@mcp.tool()
def get_forecast(latitude: float, longitude: float) -> str:
    """Ottieni le previsioni meteo correnti per una posizione.

    Args:
        latitude: Latitudine (es. 44.49).
        longitude: Longitudine (es. 11.34).
    """
    pass


@mcp.tool()
def get_weather(city: str) -> str:
    """Ottieni il meteo corrente di una città (geocoding + forecast in un colpo solo).

    Args:
        city: Nome della città (es. "Bologna").
    """
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
