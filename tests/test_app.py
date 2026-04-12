import os
import json
import pytest
from src.app import MonitorBateria

TEST_DB = 'test_bateria.json'

@pytest.fixture
def monitor():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield MonitorBateria(db_file=TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_registro_caminho_feliz(monitor):
    registro = monitor.registrar_nivel(5, "Me sentindo neutro")
    assert registro["nivel"] == 5
    assert registro["notas"] == "Me sentindo neutro"
    
    with open(TEST_DB, 'r') as f:
        dados = json.load(f)
        assert len(dados) == 1
        assert dados[0]["nivel"] == 5

def test_registro_entrada_invalida(monitor):
    with pytest.raises(ValueError, match="O nível deve ser um número inteiro entre 1 e 10."):
        monitor.registrar_nivel(11)

def test_sugestao_caso_limite(monitor):
    assert "Bateria baixa" in monitor.sugerir_acao(3)
    assert "Bateria estável" in monitor.sugerir_acao(4)