import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def monitor():
    with patch("src.app._get_supabase") as mock_supa:
        mock_client = MagicMock()
        mock_supa.return_value = mock_client
        from src.app import MonitorBateria
        m = MonitorBateria()
        m.supabase = mock_client
        yield m

def test_registro_caminho_feliz(monitor):
    monitor.supabase.table.return_value.insert.return_value.execute.return_value = None
    registro = monitor.registrar_nivel(5, "Me sentindo neutro")
    assert registro["nivel"] == 5
    assert registro["notas"] == "Me sentindo neutro"
    monitor.supabase.table("registros").insert.assert_called()

def test_registro_entrada_invalida(monitor):
    with pytest.raises(ValueError, match="O nível deve ser um número inteiro entre 1 e 10."):
        monitor.registrar_nivel(11)

def test_sugestao_caso_limite(monitor):
    assert "Bateria baixa" in monitor.sugerir_acao(3)
    assert "Bateria estável" in monitor.sugerir_acao(4)

def test_integracao_api_conselho(monitor):
    conselho = monitor.buscar_conselho_externo()
    assert isinstance(conselho, str)
    assert len(conselho) > 0