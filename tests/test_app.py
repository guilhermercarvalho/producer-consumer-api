import pytest
from src.producer_consumer_sync.app import app


@pytest.fixture
def client():
    return app.test_client()


def test_start(client):
    response = client.post('/start')
    assert response.status_code == 200
    assert response.json['id'] == 0
    # Verifique se o processo foi criado corretamente
    assert len(app.processes) == 1
    assert app.processes[0].is_alive()


def test_stop(client):
    # Crie um processo
    response = client.post('/start')
    process_id = response.json['id']

    # Pare o processo
    response = client.post(f'/stop/{process_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Processo parado'
    # Verifique se o processo foi parado corretamente
    assert not app.processes[process_id][0].is_alive()
    assert not app.processes[process_id][1].is_alive()


def test_stats(client):
    # Crie um processo
    response = client.post('/start')
    process_id = response.json['id']

    # Obtenha as estatísticas do processo
    response = client.get(f'/stats/{process_id}')
    assert response.status_code == 200
    assert 'taxa_producao' in response.json
    assert 'produzido' in response.json
    assert 'consumido' in response.json
    assert 'buffer' in response.json
    # Verifique se as estatísticas estão corretas
    assert response.json['taxa_producao'] > 0
    assert response.json['produzido'] > 0
    assert response.json['consumido'] > 0
    assert response.json['buffer'] > 0
