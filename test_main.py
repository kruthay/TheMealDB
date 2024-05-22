import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)

def test_read_meals(test_app):
    response = test_app.get("/api/meals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_meal(test_app):
    response = test_app.post("/api/meals", json={"name": "Test Meal", "category": "Test", "area": "Test Area", "instructions": "Test instructions", "tags": ["test"]})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Meal"

def test_query_meals_by_category(test_app):
    response = test_app.get("/api/meals?category=Test")
    assert response.status_code == 200
    meals = response.json()
    assert all(meal["category"] == "Test" for meal in meals)

def test_query_meals_by_area(test_app):
    response = test_app.get("/api/meals?area=Test Area")
    assert response.status_code == 200
    meals = response.json()
    assert all(meal["area"] == "Test Area" for meal in meals)

def test_query_meals_by_tags(test_app):
    response = test_app.get("/api/meals?tags=test")
    assert response.status_code == 200
    meals = response.json()
    assert all("test" in meal["tags"] for meal in meals)
