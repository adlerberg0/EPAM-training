from hw11.hw2 import Order


def morning_discount(order: Order) -> float:
    if order.client_status == "golden_client":
        return 0.3
    elif order.client_status == "silver_client":
        return 0.2
    else:
        return 0.1


def elder_discount(order: Order) -> float:
    if order.client_status == "golden_client":
        return 0.2
    elif order.client_status == "silver_client":
        return 0.1
    else:
        return 0


def test_order():
    order_1 = Order(
        100, client_status="golden_client", discount_strategy=morning_discount
    )
    assert order_1.final_price() == 70
    order_2 = Order(
        100, client_status="golden_client", discount_strategy=elder_discount
    )
    assert order_2.final_price() == 80
