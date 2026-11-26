
import pytest

from app.order_service import OrderService
from app.payment_gateway import PaymentGateway, PaymentGatewayError
from tests.support.fake_db import FakeDb


def test_error_http_500_no_registra_pedido(requests_mock):
    # ARRANGE: Preparacion
    db = FakeDb(
        stock={"CUADERNO": 10},
        prices={"CUADERNO": 25.0}
    )

    pasarela = PaymentGateway()

    respuesta_http = requests_mock.post(
        f"{pasarela.base_url}/charges",
        status_code=500,
        json={"error": "Internal Server Error"}
    )

    servicio = OrderService(db, pasarela)

    # ACT: Ejecucion
    with pytest.raises(PaymentGatewayError, match="HTTP 500"):
        servicio.place_order("CUADERNO", 2, "tok_prueba")

    # ASSERT: Comprobaciones
    assert respuesta_http.call_count == 1

    assert respuesta_http.last_request.json() == {
        "card_token": "tok_prueba",
        "amount": 58.0
    }

    assert db.orders == {}
    assert db.get_stock("CUADERNO") == 10
