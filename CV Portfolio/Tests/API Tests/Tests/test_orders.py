import requests

BASE_URL = "http://localhost:5000"

## ------------------------- TESTS FOR: /orders --------------------------------- ##

# Test - Is API accessible for user not logged in?
def test_is_API_accessible_for_anonymous_user():
    response = requests.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 401


# Test - Is API accessible for user not logged in?
def test_is_API_accessible_for_logged_in_user():
    session = requests.Session()

    login_data = {"username": "alice","password": "Password123!"}
    login = session.post(f"{BASE_URL}/api/login", json = login_data)
    assert login.status_code == 200

    response = session.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200


# Test - Is API empty for user with no orders?
def test_is_API_empty_for_orderless_logged_in_user():
    session = requests.Session()

    login_data = {"username": "alice","password": "Password123!"}
    login = session.post(f"{BASE_URL}/api/login", json = login_data)
    assert login.status_code == 200

    response = session.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200

    orders = response.json()
    assert len(orders) == 0

# Test - Is API populated for user with one orders?
def test_is_API_populated_for_single_order_logged_in_user():
    session = requests.Session()

    login_data = {"username": "alice","password": "Password123!"}
    login = session.post(f"{BASE_URL}/api/login", json = login_data)
    assert login.status_code == 200

    session.post(f"{BASE_URL}/cart/add/3")
    order = session.post(f"{BASE_URL}/checkout")
    assert order.status_code == 200

    response = session.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200

    orders = response.json()
    assert len(orders) == 1


# Test - Is data correct in order API?
def test_is_data_correct_in_order_API():
    session = requests.Session()

    login_data = {"username": "alice", "password": "Password123!"}
    login = session.post(f"{BASE_URL}/api/login", json=login_data)
    assert login.status_code == 200

    response = session.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200

    order = response.json()[0]

    assert "id" in order
    assert "items" in order
    assert "status" in order
    assert "total" in order

    assert order["items"][0]["product_id"] == 3



# Test - is API populated for user with multiple orders?
def test_is_API_populated_for_multiple_order_logged_in_user():
    session = requests.Session()

    login_data = {"username": "alice","password": "Password123!"}
    login = session.post(f"{BASE_URL}/api/login", json = login_data)
    assert login.status_code == 200

    session.post(f"{BASE_URL}/cart/add/2")
    order = session.post(f"{BASE_URL}/checkout")
    assert order.status_code == 200

    response = session.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200

    orders = response.json()
    assert len(orders) == 2