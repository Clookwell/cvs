import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.database import get_db_connection

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    """Очищення бази даних після кожного тесту"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dataset_data")
    cursor.execute("DELETE FROM datasets")
    conn.commit()
    conn.close()

def test_create_dataset():
    response = client.post("/api/datasets/", json={
        "name": "Test Dataset",
        "description": "Test Description"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Dataset"

def test_upload_data():
    # Спочатку створюємо набір даних
    create_response = client.post("/api/datasets/", json={
        "name": "Upload Test",
        "description": ""
    })
    dataset_id = create_response.json()["id"]
    
    # Тестуємо завантаження даних
    csv_data = "year,value\n2020,100\n2021,150\n2022,200"
    response = client.post(
        f"/api/datasets/{dataset_id}/upload",
        files={"file": ("data.csv", csv_data, "text/csv")}
    )
    
    assert response.status_code == 200
    assert response.json()["rows_processed"] == 3
