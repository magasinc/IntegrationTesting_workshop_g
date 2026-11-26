class FakeDb:
    """Doble de persistencia que guarda inventario y pedidos en memoria."""

    def __init__(self, stock: dict[str, int], prices: dict[str, float]):
        self._stock = dict(stock)
        self._prices = dict(prices)
        self._orders: dict[str, dict] = {}
        self._seq = 0

    def get_stock(self, product_id: str) -> int:
        return self._stock[product_id]

    def get_price(self, product_id: str) -> float:
        return self._prices[product_id]

    def save_order(self, order: dict) -> str:
        self._seq += 1
        order_id = f"ORD-{self._seq}"
        self._orders[order_id] = dict(order)
        return order_id

    def update_stock(self, product_id: str, new_stock: int) -> None:
        self._stock[product_id] = new_stock

    @property
    def orders(self) -> dict[str, dict]:
        return self._orders
