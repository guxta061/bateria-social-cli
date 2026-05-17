import json
import os
import urllib.request
from datetime import datetime

DB_FILE = 'bateria_social.json'

class MonitorBateria:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self._inicializar_banco()

    def _inicializar_banco(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def buscar_conselho_externo(self):
        """Consome a API pública Advice Slip para obter um conselho externo."""
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
        
        with open(self.db_file, 'r') as f:
            dados = json.load(f)
            
        dados.append(registro)
        
        with open(self.db_file, 'w') as f:
            json.dump(dados, f, indent=4)
        
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