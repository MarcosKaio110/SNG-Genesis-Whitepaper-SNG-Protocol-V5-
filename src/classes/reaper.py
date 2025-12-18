from src.core.base import MinerEntity
from pydantic import Field

class Reaper(MinerEntity):
    """
    A Classe Operária.
    Foco: Volume e Consistência (PVE).
    Não sofre bloqueios de 48h, mas minera menos por unidade sem upgrades.
    """
    tool_level: int = Field(default=1, ge=1) # Nível da Picareta (Minimo 1)
    blocks_mined: int = 0

    def calculate_mining_power(self) -> float:
        """
        Força Bruta = Base (20) + (Nível da Ferramenta * 5)
        Reaper começa mais forte que Eremita, mas escala linearmente.
        """
        base_power = 20.0
        gear_bonus = self.tool_level * 5.0
        return base_power + gear_bonus

    def perform_cycle_action(self) -> dict:
        """
        O Reaper apenas trabalha.
        Simula a mineração de um bloco padrão.
        """
        power = self.calculate_mining_power()
        # Simulação simples de ganho baseada na força
        yield_amount = power * 0.5 
        
        self.add_balance(yield_amount)
        self.blocks_mined += 1
        
        return {
            "status": "MINING",
            "msg": f"Bloco processado com força {power}. Rendimento: {yield_amount:.2f} SNG."
        }

    def upgrade_tool(self) -> str:
        """Gasta SNG para melhorar a ferramenta permanentemente."""
        cost = self.tool_level * 100
        if self.get_balance() >= cost:
            self._sng_balance -= cost # Acessa direto pois está na classe filha
            self.tool_level += 1
            return f"Upgrade Sucesso! Picareta Nível {self.tool_level}."
        else:
            return "Saldo insuficiente para upgrade."
