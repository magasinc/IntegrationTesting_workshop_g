from app import cli
from app.order_service import OrderService


def test_cli_confirma_pedido(mocker, capsys):
    servicio = mocker.Mock(spec=OrderService)
    servicio.place_order.return_value = {
        "order_id": "ORD-7",
        "total": 58.0,
        "status": "CONFIRMED",
    }
    # Sustituimos el servicio donde la CLI lo construye.
    mocker.patch("app.cli.build_service", return_value=servicio)

    mocker.patch("builtins.input", side_effect=["CUADERNO", "2", "tok_ejemplo"])
    codigo = cli.main()

    assert codigo == 0
    assert capsys.readouterr().out == "OK: pedido ORD-7 confirmado, total=58.0\n"
    servicio.place_order.assert_called_once_with("CUADERNO", 2, "tok_ejemplo")
