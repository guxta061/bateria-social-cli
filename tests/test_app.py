import os
import json
import pytest
from src.app import MonitorBateria

# Arquivo de teste temporário para não sujar o banco principal
TEST_DB = 'test_bateria.json'

@pytest.fixture
def monitor():
    """Fixture que prepara um monitor limpo antes de cada teste."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield MonitorBateria(db_file=TEST_DB)
    
    # Limpeza após o teste
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_registro_caminho_feliz(monitor):
    """Teste 1: Cenário de uso correto (Caminho feliz)."""
    registro = monitor.registrar_nivel(5, "Me sentindo neutro")
    assert registro["nivel"] == 5
    assert registro["notas"] == "Me sentindo neutro"
    
    # Verifica se realmente salvou no arquivo JSON
    with open(TEST_DB, 'r') as f:
        dados = json.load(f)
        assert len(dados) == 1
        assert dados[0]["nivel"] == 5

def test_registro_entrada_invalida(monitor):
    """Teste 2: Entrada inválida ou comportamento indevido."""
    # Tenta passar um nível acima de 10 e espera um erro
    with pytest.raises(ValueError, match="O nível deve ser um número inteiro entre 1 e 10."):
        monitor.registrar_nivel(11)

def test_sugestao_caso_limite(monitor):
    """Teste 3: Caso limite da funcionalidade principal."""
    # Testa exatamente a fronteira onde a bateria muda de baixa para estável
    assert "Bateria baixa" in monitor.sugerir_acao(3)
    assert "Bateria estável" in monitor.sugerir_acao(4)