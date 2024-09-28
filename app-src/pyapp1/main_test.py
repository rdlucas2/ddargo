from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_read_item_without_query():
    """Test the /items/{item_id} endpoint without query parameter."""
    item_id = 1
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": None}

def test_read_item_with_query():
    """Test the /items/{item_id} endpoint with query parameter."""
    item_id = 2
    query = "test_query"
    response = client.get(f"/items/{item_id}?q={query}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": query}
