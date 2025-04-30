import os
from dotenv import load_dotenv
import requests
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel

CONFIG_FILE = os.path.expanduser("~/.guarani_coti_config")
console = Console()


def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            key = f.read().strip()
            if key:
                return key
    return None


def save_api_key(key):
    with open(CONFIG_FILE, "w") as f:
        f.write(key.strip())


def get_api_key():
    load_dotenv()  # carga variables de .env si existen
    api_key = os.getenv("EXCHANGE_RATE_API_KEY") or load_api_key()
    if not api_key:
        api_key = console.input("[yellow]Por favor ingresa tu EXCHANGE_RATE_API_KEY (o Enter para None): [/yellow]").strip()
        save_api_key(api_key)
        console.print("[green]API key guardada para futuras ejecuciones en ~/.guarani_coti_config[/green]")
    return api_key


API_KEY = get_api_key()

currencies = ["ARS", "BRL", "MXN", "EUR"]


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
    if not API_KEY:
        return {}
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/PYG"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("result") == "success":
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
    if exchange_rates:
        for cur, rate in exchange_rates.items():
            if rate:
                valor = 1 / rate if rate != 0 else 0
                table2.add_row(cur, f"{valor:,.2f}")
            else:
                table2.add_row(cur, "-")
    else:
        table2.add_row("-", "No disponible")

    console.print(Columns([Panel(table1), Panel(table2)]))


if __name__ == "__main__":
    main()
