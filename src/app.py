import os
import urllib.request
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
def _get_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL e SUPABASE_KEY devem estar definidos.")
    return create_client(url, key)

class MonitorBateria:
    def __init__(self, db_file=None):
        self.supabase = _get_supabase()

    def buscar_conselho_externo(self):
        url = "https://api.adviceslip.com/advice"
        try:
            with urllib.request.urlopen(url, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    return data["slip"]["advice"]
        except Exception:
            return "Respire fundo e respeite os limites da sua bateria social."
        return "Tire um tempo para você descansar."

    def registrar_nivel(self, nivel, notas=""):
        if not isinstance(nivel, int) or not (1 <= nivel <= 10):
            raise ValueError("O nível deve ser um número inteiro entre 1 e 10.")

        registro = {
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": nivel,
            "notas": notas
        }

        self.supabase.table("registros").insert(registro).execute()
        return registro

    def sugerir_acao(self, nivel):
        if nivel <= 3:
            return "Alerta: Bateria baixa! Sugestão: Foque em tarefas isoladas."
        elif nivel <= 7:
            return "Bateria estável. Interações moderadas são bem-vindas."
        else:
            return "Bateria alta! Ótimo momento para networking e colaboração."

def main():
    monitor = MonitorBateria()
    print("=== Monitor de Bateria Social ===")
    try:
        entrada = input("Qual seu nível de bateria social agora (1 a 10)? ")
        nivel = int(entrada)
        notas = input("Alguma nota sobre como se sente? (Opcional): ")
        monitor.registrar_nivel(nivel, notas)
        print("\n✅ Registro salvo com sucesso!")
        print(f"💡 Dica do sistema: {monitor.sugerir_acao(nivel)}")
        print("\n🌐 Buscando pílula de sabedoria da internet...")
        conselho = monitor.buscar_conselho_externo()
        print(f"✨ Conselho do dia (API): {conselho}")
    except ValueError as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()