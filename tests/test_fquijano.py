from app import cli
from app.order_service import OrderService
from app.payment_gateway import PaymentGateway
from tests.support.fake_db import FakeDb

def test_pedido_aprobado_con_iva(mocker, capsys):
    # Arrange
    db = FakeDb(
        stock={"CUADERNO": 10},
        prices={"CUADERNO": 25.0}
    )

    gateway = mocker.Mock(spec=PaymentGateway)
    gateway.charge.return_value = {
        "approved": True,
        "transaction_id": "tx_001"
    }

    service = OrderService(db, gateway)

    mocker.patch("app.cli.build_service", return_value=service)
    mocker.patch(
        "builtins.input",
        side_effect=["CUADERNO", "2", "tok_001"]
    )

    # Act
    result = cli.main()

    # Assert
    assert result == 0
    assert capsys.readouterr().out == (
        "OK: pedido ORD-1 confirmado, total=58.0\n"
    )

    gateway.charge.assert_called_once_with("tok_001", 58.0)

    assert db.orders["ORD-1"]["total"] == 58.0
    assert db.orders["ORD-1"]["transaction_id"] == "tx_001"