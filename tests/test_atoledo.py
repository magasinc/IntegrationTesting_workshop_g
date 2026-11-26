import pytest

from app.order_service import OrderService, PaymentRejectedError
from app.payment_gateway import PaymentGateway
from tests.support.fake_db import FakeDb


def test_pago_rechazado_no_registra_pedido(mocker):
    db = FakeDb(stock={"TAZA": 9}, prices={"TAZA": 7.5})
    pasarela = mocker.Mock(spec=PaymentGateway)
    pasarela.charge.return_value = {"approved": False, "reason": "fondos insuficientes"}
    servicio = OrderService(db, pasarela)

    with pytest.raises(PaymentRejectedError):
        servicio.place_order("TAZA", 2, "tok_prueba")

    pasarela.charge.assert_called_once_with("tok_prueba", 17.4)
    assert db.orders == {}
    assert db.get_stock("TAZA") == 9
