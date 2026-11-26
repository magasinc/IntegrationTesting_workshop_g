import pytest

from app.order_service import OrderService, OutOfStockError
from app.payment_gateway import PaymentGateway
from tests.support.fake_db import FakeDb


def test_stock_insuficiente_no_intenta_cobrar(mocker):
    db = FakeDb(stock={"TAZA": 1}, prices={"TAZA": 7.5})
    pasarela = mocker.Mock(spec=PaymentGateway)
    servicio = OrderService(db, pasarela)

    with pytest.raises(OutOfStockError, match="Stock insuficiente"):
        servicio.place_order("TAZA", 2, "tok_prueba")

    pasarela.charge.assert_not_called()
    assert db.orders == {}
    assert db.get_stock("TAZA") == 1
 