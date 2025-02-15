import pytest

from producer_consumer_sync.app_old import app


@pytest.fixture
def client():
    return app.test_client()


def test_start(client):
    response = client.post("/start")
    assert response.status_code == 200
    assert response.json["id"] == 0
    # Verifique se o processo foi criado corretamente
    assert len(app.processes) == 1


def test_stop(client):
    # Crie um processo
    response = client.post("/start")
    process_id = response.json["id"]

    # Pare o processo
    response = client.post(f"/stop/{process_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Processo parado"
    # Verifique se o processo foi parado corretamente
    assert process_id not in app.processes


def test_stats(client):
    # Crie um processo
    response = client.post("/start")
    process_id = response.json["id"]

    # Obtenha as estatísticas do processo
    response = client.get(f"/stats/{process_id}")
    assert response.status_code == 200
    assert "production" in response.json
    assert "consumption" in response.json
    # Verifique se as estatísticas estão corretas
    assert "quantity" in response.json["production"]
    assert "rate" in response.json["production"]
    assert "quantity" in response.json["consumption"]
    assert "rate" in response.json["consumption"]
