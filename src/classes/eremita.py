from datetime import datetime, timedelta
from typing import Literal
from src.core.base import MinerEntity

# Define que os níveis só podem ser 1, 2, 3, 4 ou 5
EremitaLevel = Literal[1, 2, 3, 4, 5]

class Eremita(MinerEntity):
    level: EremitaLevel = 1
    wisdom_streak: int = 0  # Dias seguidos sem errar

    def calculate_mining_power(self) -> float:
        """
        Eremita foca em multiplicadores, não em força bruta.
        Base baixa (10) * Multiplicador do Nível.
        """
        base_power = 10.0
        # Tabela de Multiplicadores do GDD
        multipliers = {1: 1.0, 2: 1.5, 3: 2.5, 4: 5.0, 5: 10.0}
        return base_power * multipliers[self.level]

    def perform_cycle_action(self) -> dict:
        """Verifica se está bloqueado antes de deixar jogar."""
        if self.is_locked and self.lock_until:
             if datetime.now() < self.lock_until:
                 remaining = self.lock_until - datetime.now()
                 # Formata o tempo restante para horas:minutos
                 hours, remainder = divmod(remaining.seconds, 3600)
                 minutes, _ = divmod(remainder, 60)
                 return {
                     "status": "LOCKED", 
                     "msg": f"Mente nublada. Retorne em {remaining.days}d {hours}h {minutes}m."
                 }
             else:
                 # O tempo passou, desbloqueia
                 self.is_locked = False
                 self.lock_until = None
        
        return {"status": "READY", "msg": "A Sala de Meditação aguarda seu intelecto."}

    def apply_pvp_penalty(self, level_attempted: int) -> None:
        """
        Aplica a Punição do GDD:
        Tempo = 48 horas + Nível Disputado
        """
        penalty_hours = 48 + level_attempted
        self.lock_until = datetime.now() + timedelta(hours=penalty_hours)
        self.is_locked = True
        
        print(f"\n[SISTEMA] 🚫 PUNIÇÃO APLICADA!")
        print(f"Motivo: Falha no teste de nível {level_attempted}.")
        print(f"Bloqueio: {penalty_hours} horas (48h base + {level_attempted}h nível).")
