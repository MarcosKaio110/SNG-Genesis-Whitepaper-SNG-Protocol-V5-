from src.core.chronos import ChronosOracle
import random
import time

def main():
    oracle = ChronosOracle()
    
    print("=== ⏳ INICIANDO PROTOCOLO CHRONOS ===")
    print("Obs: Um desperto aguarda. Simulando varredura...")
    
    # Escolhe um ponto aleatório no tempo (i)
    random_moment = random.randint(0, 90)
    
    result = oracle.sync_reality(start_index_i=random_moment)
    
    # Efeito de suspense (Anti-Dopamina Barata)
    time.sleep(2) 
    
    if result['status'] == "SYNCED":
        print("\n🔓 REALIDADE DECODIFICADA!")
        print(result['msg'])
        print(f"O Universo alinhou no segundo: {result['time_offset']}")
    else:
        print("\n🌫️ Mente desconexa.")
        print(result['msg'])

if __name__ == "__main__":
    main()
