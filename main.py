from src.classes.eremita import Eremita
from src.classes.reaper import Reaper
from src.classes.vampire import Vampire
import random

def main():
    print("\n=== 🩸 SIMULAÇÃO DE ECOSSISTEMA EREMITA ===")

    # 1. Criar os Personagens
    reaper = Reaper(wallet_id="0xWorker", nickname="Miner_Bob")
    vampire = Vampire(wallet_id="0xDracula", nickname="Alucard")
    
    # 2. O Reaper trabalha (Gera riqueza)
    print(f"\n[REAPER] {reaper.nickname} começou o turno...")
    reaper_action = reaper.perform_cycle_action()
    print(f" > {reaper_action['msg']}")
    print(f" > Saldo Atual: {reaper.get_balance()} SNG")
    
    # Vamos dar um bônus fictício para o Reaper (Ex: Guilda)
    bonus_da_guilda = 50.0 
    print(f" > [BÔNUS] Guilda aplicou +{bonus_da_guilda} SNG extra (Pendente).")

    # 3. O Vampiro Acorda
    print(f"\n[VAMPIRE] {vampire.nickname} iniciou o ciclo de caça...")
    hunt_result = vampire.perform_cycle_action()
    print(f" > Status: {hunt_result['status']}")
    print(f" > {hunt_result['msg']}")

    # 4. Simulação de Encontro (Se for Stealth, ele rouba)
    # Vamos forçar um ataque Stealth para testar a queima
    if hunt_result['mode'] == "STEALTH" or True: # O 'or True' é forçar o teste agora
        print("\n--- ⚠️  ENCONTRO DETECTADO ---")
        print(f"O Vampiro encontrou {reaper.nickname}!")
        
        # O Vampiro drena
        # Ele rouba o que o Reaper minerou (reaper.get_balance) e queima o bonus
        drain_report = vampire.execute_stealth_drain(
            victim_base_drop=reaper.get_balance(),
            victim_bonus=bonus_da_guilda
        )
        
        print(f"RESULTADO DO ATAQUE:")
        print(f"💰 Vampiro Ganhou: {drain_report['stolen']} SNG")
        print(f"🔥 Economia Queimou: {drain_report['burned']} SNG (Bônus Evaporado)")
        print(f"💀 Reaper Perdeu Tudo.")
        
        # Na prática, zeraríamos o saldo do Reaper aqui, mas deixei visual por enquanto.

if __name__ == "__main__":
    main()
