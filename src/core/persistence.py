import json
import os
from src.classes.eremita import Eremita
from src.classes.reaper import Reaper

class SaveManager:
    """Gerencia Salvar e Carregar o jogo em JSON."""
    
    @staticmethod
    def save_game(player) -> str:
        """Salva o estado atual do jogador."""
        # Converte o objeto jogador em um Dicionário Python
        data = player.model_dump(mode='json')
        
        # Adiciona manualmente o saldo (que é privado) e o tipo da classe
        data['_sng_balance'] = player.get_balance()
        data['class_type'] = player.__class__.__name__
        
        # Caminho do arquivo
        filepath = f"data/{player.wallet_id}.json"
        
        # Grava no disco
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4, default=str)
            
        return f"Progresso salvo em {filepath}"

    @staticmethod
    def load_game(wallet_id: str, class_type: str):
        """Carrega o jogo ou retorna None se não existir save."""
        filepath = f"data/{wallet_id}.json"
        
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, "r") as f:
            data = json.load(f)
            
        # Recria o objeto correto (Reaper ou Eremita)
        if class_type == "Eremita":
            player = Eremita(**data)
        else:
            player = Reaper(**data)
            
        # Restaura o saldo (que estava protegido)
        player.set_balance_from_save(data.get('_sng_balance', 0.0))
        return player
