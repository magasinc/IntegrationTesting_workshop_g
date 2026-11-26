"""Interfaz de línea de comandos de OrderSystem."""

from app.db_connector import DbConnector
from app.order_service import OrderService, OutOfStockError, PaymentRejectedError
from app.payment_gateway import PaymentGateway


def build_service() -> OrderService:
    return OrderService(DbConnector(), PaymentGateway())


def run_order(service: OrderService, product_id: str, quantity: int, card_token: str) -> str:
    """Procesa el pedido y devuelve el mensaje para el usuario."""
    try:
        result = service.place_order(product_id, quantity, card_token)
    except OutOfStockError as exc:
        return f"ERROR: sin stock ({exc})"
    except PaymentRejectedError as exc:
        return f"ERROR: pago rechazado ({exc})"
    except Exception as exc:  # noqa: BLE001 - la CLI nunca debe reventar.
        return f"ERROR: inesperado ({exc})"

    return f"OK: pedido {result['order_id']} confirmado, total={result['total']}"


def main() -> int:
    product_id = input("Código del producto: ").strip().upper()

    try:
        quantity = int(input("Cantidad: "))
    except ValueError:
        print("ERROR: la cantidad debe ser un número entero.")
        return 1

    card_token = input("Token de pago: ").strip()
    service = build_service()
    message = run_order(service, product_id, quantity, card_token)
    print(message)

    if message.startswith("OK:"):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
