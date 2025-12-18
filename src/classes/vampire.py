import random
from typing import Literal
from src.core.base import MinerEntity

# Modos de Caça Possíveis
HuntMode = Literal["BUTCHER", "MIND_EATER", "HYBRID", "STEALTH"]

class Vampire(MinerEntity):
    """
    A Classe Evento (1 a cada 24h).
    Não minera. Rouba.
    """
    victims_claimed: int = 0
    sun_exposure: int = 0 # Contador para Game Over (Protocolo Amanhecer)

    def calculate_mining_power(self) -> float:
        # Vampiros não mineram hashes.
        return 0.0

    def perform_cycle_action(self) -> dict:
        """
        Roda a roleta RNG para definir como o Vampiro vai atacar nesta rodada.
        """
        roll = random.random() * 100 # 0 a 100
        
        mode: HuntMode
        msg: str
        
        if roll <= 1.0: # 1% de chance
            mode = "STEALTH"
            msg = "👁️ SOMBRA PURA ATIVA. Buscando Hash de Sangue..."
        elif roll <= 34.0: # ~33%
            mode = "BUTCHER"
            msg = "Modo Açougueiro: Caçando Reapers."
        elif roll <= 67.0: # ~33%
            mode = "MIND_EATER"
            msg = "Modo Devorador: Caçando Eremitas."
        else:
            mode = "HYBRID"
            msg = "Modo Híbrido: Caça Aleatória."
            
        return {"status": "HUNTING", "mode": mode, "msg": msg}

    def execute_stealth_drain(self, victim_base_drop: float, victim_bonus: float) -> dict:
        """
        MECÂNICA ANTI-INFLAÇÃO:
        O Vampiro rouba a BASE.
        O Bônus da vítima é QUEIMADO (desaparece da economia).
        """
        # 1. Rouba o valor base
        self.add_balance(victim_base_drop)
        self.victims_claimed += 1
        
        total_removed_from_economy = victim_base_drop + victim_bonus
        
        return {
            "stolen": victim_base_drop,
            "burned": victim_bonus,
            "total_impact": total_removed_from_economy,
            "msg": f"Drenado {victim_base_drop} SNG. Bônus de {victim_bonus} foi EVAPORADO."
        }
