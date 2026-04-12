import json
import os
from datetime import datetime

DB_FILE = 'bateria_social.json'

class MonitorBateria:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self._inicializar_banco()

    def _inicializar_banco(self):
        """Cria o arquivo JSON se ele não existir."""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def registrar_nivel(self, nivel, notas=""):
        """Registra o nível atual e salva no JSON."""
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
        """Retorna uma sugestão baseada no nível de energia."""
        if nivel <= 3:
            return "Alerta: Bateria baixa! Sugestão: Foque em tarefas isoladas e adie reuniões não urgentes."
        elif nivel <= 7:
            return "Bateria estável. Interações moderadas são bem-vindas, mas respeite seus limites."
        else:
            return "Bateria alta! Ótimo momento para networking, colaboração e tarefas em equipe."

def main():
    monitor = MonitorBateria()
    print("=== Monitor de Bateria Social ===")
    print("Bem-vindo! Vamos mapear sua energia social hoje.\n")
    
    try:
        entrada = input("Qual seu nível de bateria social agora (1 a 10)? ")
        nivel = int(entrada)
        notas = input("Alguma nota sobre como se sente? (Opcional): ")
        
        monitor.registrar_nivel(nivel, notas)
        
        print("\n✅ Registro salvo com sucesso!")
        print(f"💡 Dica do sistema: {monitor.sugerir_acao(nivel)}")
        
    except ValueError as e:
        if "invalid literal" in str(e):
             print("❌ Erro: Por favor, digite apenas números inteiros.")
        else:
             print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()