from pydantic import BaseModel
from typing import Set

class ChronosOracle(BaseModel):
    """
    O MOTOR DA REALIDADE V3.
    Define a raridade dos drops temporais baseados em Fibonacci.
    """
    _fib_set: Set[int] = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144}
    # Pi simulado (Vetor Infinito)
    _pi_vector: str = "3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067"

    def calculate_digital_root(self, n: int) -> int:
        return 1 + (n - 1) % 9 if n else 0

    def sync_reality(self, start_index_i: int) -> dict:
        safe_i = start_index_i % len(self._pi_vector)
        val_at_i = int(self._pi_vector[safe_i])
        seed_s1 = val_at_i + safe_i
        
        # Varredura simulada
        for k in range(1, 301):
            future_idx = (safe_i + k) % len(self._pi_vector)
            val_at_k = int(self._pi_vector[future_idx])
            
            complex_sum = seed_s1 + val_at_k + k
            root = self.calculate_digital_root(complex_sum)
            
            if root in self._fib_set:
                # --- SISTEMA DE RARIDADE ---
                if root >= 13:
                    item = "NFT_ARTEFATO_ETERNO (Permanente)"
                    bonus = 1000.0
                elif root >= 5:
                    item = "FRASCO_DE_FLUXO (Buff 24h)"
                    bonus = 100.0
                else:
                    item = "INSIGHT_MOMENTANEO (Buff 1h)"
                    bonus = 20.0

                return {
                    "status": "SYNCED",
                    "fibonacci_found": root,
                    "reward_item": item,
                    "sng_value": bonus,
                    "msg": f"Sincronicidade em {k}s! Raiz {root}."
                }

        return {"status": "NOISE", "msg": "Apenas ruído estático. O caos venceu."}
