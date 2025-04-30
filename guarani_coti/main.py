import requests
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel

load_dotenv()

# API key para ExchangeRate-API
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
if not API_KEY:
    raise ValueError("Falta la variable EXCHANGE_RATE_API_KEY en .env")

# Monedas a consultar frente a PYG
currencies = ["ARS", "BRL", "MXN", "EUR"]

console = Console()

def get_dolarpy_quotes():
    url = "https://dolar.melizeche.com/api/1.0/"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("dolarpy", {})
    except Exception as e:
        console.print(f"[red]Error al obtener cotizaciones dólar-guaraní: {e}[/red]")
        return {}

def get_exchange_rates():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/PYG"
    try:
        response = requests.get(url)
        data = response.json()
        if data["result"] == "success":
            return {cur: data["conversion_rates"].get(cur, None) for cur in currencies}
        else:
            console.print(f"[red]Error en ExchangeRate-API: {data.get('error-type', 'Desconocido')}[/red]")
            return {}
    except Exception as e:
        console.print(f"[red]Error al obtener cotizaciones ExchangeRate-API: {e}[/red]")
        return {}


def main():
    console.print("[bold green]Obteniendo cotizaciones...[/bold green]\n")
    dolarpy_quotes = get_dolarpy_quotes()
    exchange_rates = get_exchange_rates()

    table1 = Table(title="Cotizaciones Dólar (USD) - Guaraní (PYG) en Paraguay")
    table1.add_column("Casa de Cambio", style="cyan", no_wrap=True)
    table1.add_column("Compra (PYG)", justify="right")
    table1.add_column("Venta (PYG)", justify="right")
    for casa, valores in dolarpy_quotes.items():
        compra = f"{valores.get('compra', 0):,.2f}" if valores.get('compra', 0) else "-"
        venta = f"{valores.get('venta', 0):,.2f}" if valores.get('venta', 0) else "-"
        table1.add_row(casa.capitalize(), compra, venta)

    table2 = Table(title="Cotizaciones Guaraní (PYG) frente a otras monedas")
    table2.add_column("Moneda", style="magenta")
    table2.add_column("Valor 1 PYG en moneda", justify="right")
    for cur, rate in exchange_rates.items():
        if rate:
            valor = 1 / rate if rate != 0 else 0
            table2.add_row(cur, f"{valor:,.2f}")
        else:
            table2.add_row(cur, "-")

    # Mostrar las dos tablas lado a lado usando Columns y Panel para bordes
    console.print(Columns([Panel(table1), Panel(table2)]))


if __name__ == "__main__":
    main()
