from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, PrivateAttr

# ID PÚBLICO DA CARTEIRA DO ARQUITETO (Fundo de Desenvolvimento/Humanitário)
ARCHITECT_WALLET_ID = "0xGenesis_Architect_Fund_42"

class MinerEntity(BaseModel, ABC):
    """
    Classe Base com Entropia, Rastreamento de Atividade e Persistência.
    """
    wallet_id: str
    nickname: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    # RASTREAMENTO DE ATIVIDADE (Para a Taxa de Manutenção)
    last_activity: datetime = Field(default_factory=datetime.now)
    
    # Saldo privado (Protegido)
    _sng_balance: float = PrivateAttr(default=0.0)
    
    is_locked: bool = False
    lock_until: Optional[datetime] = None

    def get_balance(self) -> float:
        return self._sng_balance
    
    def set_balance_from_save(self, amount: float):
        """Usado apenas pelo sistema de Load para restaurar saldo."""
        self._sng_balance = amount

    def add_balance(self, amount: float) -> None:
        """Adicionar saldo conta como atividade e reseta o timer."""
        if amount != 0:
            self._sng_balance += amount
            self.refresh_activity()

    def refresh_activity(self):
        """Atualiza a data da última transação para AGORA."""
        self.last_activity = datetime.now()

    def check_entropy_tax(self) -> dict:
        """
        A LEI DA ENTROPIA (V2):
        Calcula se o jogador está AFK e aplica a taxa de 1%.
        """
        now = datetime.now()
        account_age_days = (now - self.created_at).days
        inactive_time = now - self.last_activity
        
        # REGRA DE TOLERÂNCIA
        if account_age_days < 7:
            # Novatos: Tolerância curta (24h) para criar hábito
            max_inactive = timedelta(hours=24)
            status = "NOVATO (Risco Diário)"
        else:
            # Veteranos: Direito a Férias (30 Dias)
            max_inactive = timedelta(days=30)
            status = "VETERANO (Imunidade 30 Dias)"

        if inactive_time > max_inactive:
            # APLICAR TAXA DE 1%
            tax_amount = self._sng_balance * 0.01
            
            # Limpeza de poeira (Dusting) se for valor irrisório
            if tax_amount < 0.01 and self._sng_balance > 0: 
                tax_amount = self._sng_balance

            self._sng_balance -= tax_amount
            
            # 50% vai para o Arquiteto (Fundo Humanitário), 50% é Queimado
            to_architect = tax_amount * 0.5
            
            return {
                "applied": True,
                "tax": tax_amount,
                "architect": to_architect,
                "msg": f"⚠️ ENTROPIA APLICADA! -{tax_amount:.4f} SNG (Inatividade)."
            }
        
        return {"applied": False, "msg": "Carteira Ativa. Entropia contida.", "status": status}

    @abstractmethod
    def calculate_mining_power(self) -> float:
        pass

    @abstractmethod
    def perform_cycle_action(self) -> dict:
        pass
