from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_get_info_by_date():
    response = client.get("/report?date=2019-08-01")
    assert response.status_code == 200
    assert response.json() == {
        "customers": 9,
        "total_discount_amount": 15.155224454657548,
        "items": 2895,
        "order_total_avg": 1182286.0960463746,
        "discount_rate_avg": 0.12524978888146734,
        "commissions": {
            "promotions": {
                "3": 9667019.012878517,
                "4": 0.0,
                "2": 3048059.700865304,
                "5": 2157810.5181174576},
            "total": 258932477.8951165,
            "order_average": 28770275.32167961
        }
    }