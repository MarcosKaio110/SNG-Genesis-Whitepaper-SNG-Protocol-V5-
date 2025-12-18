class RewardCalculator:
    """
    MOTOR ECONÔMICO V12.0 (Com Estimativa Prévia)
    """
    BASE_VALUE = 0.50
    
    @staticmethod
    def get_base_for_level(level: int) -> float:
        """Retorna a base crua do nível."""
        if level <= 10: return (level / 10.0) * RewardCalculator.BASE_VALUE
        if level == 11: return 1.25
        if level == 12: return 1.58
        if level == 13: return 2.00
        if level == 14: return 2.50
        if level == 15: return 3.25
        if level == 16: return 4.00
        if level == 17: return 5.00
        if level == 18: return 6.66
        return 0.1

    @staticmethod
    def estimate_potential(level: int, player_class: str, is_rift: bool = False, pile_bonus: float = 0.0) -> str:
        """Gera o texto de marketing para o HUD antes do puzzle."""
        base = RewardCalculator.get_base_for_level(level) + pile_bonus
        multiplier = 1.0
        
        tags = []
        if player_class == "Reaper": 
            multiplier += 0.50
            tags.append("REAPER")
        
        if is_rift:
            multiplier += 0.20
            tags.append("RIFT")

        # Valor estimado (sem contar speed kill que só sabemos no final)
        estimated = base * multiplier
        
        txt = f"{estimated:.4f} SNG"
        if tags: txt += f" ({' + '.join(tags)})"
        if player_class == "Reaper": txt += " [+ Speed Bonus]"
        
        return txt

    @staticmethod
    def calculate(level: int, time_taken: float, player_class: str, pile_bonus: float = 0.0, is_rift: bool = False) -> dict:
        # Cálculo Final Real
        base = RewardCalculator.get_base_for_level(level) + pile_bonus
        multiplier = 1.0
        breakdown = []

        if player_class == "Reaper":
            multiplier += 0.50
            breakdown.append("Reaper (+50%)")
            if time_taken < 9.9:
                multiplier += 0.01
                breakdown.append("Speed (+1%)")

        if is_rift:
            multiplier += 0.20
            breakdown.append("Fenda (+20%)")

        total = base * multiplier
        return {"total": round(total, 4), "base": round(base, 4), "breakdown": ", ".join(breakdown)}
