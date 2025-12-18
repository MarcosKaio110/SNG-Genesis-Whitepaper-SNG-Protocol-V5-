import random
import math
import unicodedata
import os
from typing import Tuple, List, Set

# --- ARSENAL ---
SIGIL_COMBINERS = ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306', '\u0332', '\u0333', '\u0334', '\u0335', '\u0336', '\u0337', '\u0338']
HIPERSIGILO_MAP = {
    'A': ['A', '4', '@', '/-\\', 'Ã'], 'B': ['B', '8', '|3', 'ß'], 
    'C': ['C', '(', '<', '©', '{'], 'D': ['D', '|)', 'd3', 'Ð'], 
    'E': ['E', '3', '€', '£', 'Ë'], 'F': ['F', '|=', 'ƒ', 'ph'],
    'G': ['G', '6', '9', '&'], 'H': ['H', '#', '|-|', '}{'], 
    'I': ['I', '!', '|', '1', '¡'], 'J': ['J', '_|', '¿'], 
    'K': ['K', '|<', 'X'], 'L': ['L', '|_', '1', '£'],
    'M': ['M', '/\\/\\', 'AA', 'IVI'], 'N': ['N', '/\\/', '^/', 'π'], 
    'O': ['O', '0', '()', '°', 'Ø'], 'P': ['P', '|*', '¶', '?'], 
    'Q': ['Q', '9', 'O,', 'kw'], 'R': ['R', '|2', '®', 'Я'],
    'S': ['S', '$', '5', '§', 'z'], 'T': ['T', '7', '+', '†'], 
    'U': ['U', '|_|', 'µ'], 'V': ['V', '\\/', 'v'], 
    'W': ['W', '\\/\\/', 'vv'], 'X': ['X', '><', '%', '*'],
    'Y': ['Y', '¥', 'j'], 'Z': ['Z', '2', '%']
}
RUIDO_CHARS = ['.', ',', ';', ':', '-', '_', '+', '=', '*', '&', '%', '$', '#', '@', '!', '?']
DEFAULT_LEXICO = ["SINGULARIDADE", "SISTEMA", "IMPERIO", "CONTROLE", "REALIDADE", "MATRIX", "HUMANO", "FIBONACCI", "CAOS", "ENTROPIA", "NEXUS", "EREMITA"]

class NexusEngine:
    """
    O MOTOR v11.0 (Phantom Mode)
    Nível 10-13: Sinal Colorido Fragmentado vs Ruído Cinza.
    Nível 14+: Caos Total (Hardcore).
    """
    PALETA_NEON = ["bold cyan", "bold yellow", "bold green", "bold magenta", "bold white", "bold orange"]
    
    def __init__(self):
        self.lexico = []
        self.carregar_lexico()

    def carregar_lexico(self):
        if os.path.exists("corpus_caos.txt"):
            try:
                with open("corpus_caos.txt", "r") as f:
                    self.lexico = [l.strip().upper() for l in f if len(l.strip()) > 3]
            except: pass
        if not self.lexico: self.lexico = DEFAULT_LEXICO

    def sanitizar(self, texto: str) -> str:
        return texto.replace("[", "(").replace("]", ")")

    def construir_glifo(self, char_original: str, nivel: int) -> str:
        char_safe = self.sanitizar(char_original)
        chance = min(0.95, nivel * 0.08)
        if char_safe in HIPERSIGILO_MAP and random.random() < chance:
            return self.sanitizar(random.choice(HIPERSIGILO_MAP[char_safe]))
        return char_safe

    def renderizar_palavra(self, texto: str, nivel: int, is_target: bool) -> str:
        chars = list(texto)
        final_output = []
        
        # Fatores de Ruído
        densidade_ruido = 0.5 if nivel >= 5 else 0.1
        if nivel >= 14: densidade_ruido = 1.0 # Caos total

        for i, char_original in enumerate(chars):
            glifo = self.construir_glifo(char_original, nivel)
            
            # Zalgo apenas se for alvo (para dar corpo) ou Nível 14+
            if (is_target or nivel >= 14) and nivel >= 3 and random.random() < 0.1:
                glifo += random.choice(SIGIL_COMBINERS)

            # --- LÓGICA DE COR (A Grande Mudança) ---
            tag_cor = ""

            # MODO PHANTOM (10 a 13): Contraste Alto
            if 10 <= nivel <= 13:
                if is_target:
                    # 70% Neon (Sinal), 30% Cinza (Camuflagem)
                    if random.random() < 0.7:
                        tag_cor = f"[{random.choice(self.PALETA_NEON)}]"
                    else:
                        tag_cor = "[dim white]" # Camuflagem espectral
                else:
                    # Ruído/Traps são estritamente escuros para não confundir
                    tag_cor = "[dim grey]"

            # MODO VOID (14+): Caos Total (Tudo brilha ou nada brilha)
            elif nivel >= 14:
                 tag_cor = f"[{random.choice(self.PALETA_NEON)}]" if random.random() < 0.5 else "[dim]"

            # MODO PADRÃO (1-9): Fibonacci ou Simples
            else:
                if is_target:
                    is_anchor = (i % 2 == 0) # Simplificado para teste
                    tag_cor = f"[{random.choice(self.PALETA_NEON)}]" if is_anchor else "[dim]"
                else:
                    tag_cor = "[dim red]" # Traps vermelhas nos níveis baixos

            final_output.append(f"{tag_cor}{glifo}[/]")

            # Injeção de Ruído entre letras
            if random.random() < (densidade_ruido * 0.8):
                lixo = self.sanitizar(random.choice(RUIDO_CHARS))
                # No Phantom Mode, lixo é sempre escuro
                cor_lixo = "[dim]"
                if nivel >= 14: cor_lixo = f"[{random.choice(self.PALETA_NEON)}]" # Só no Void o lixo brilha
                
                final_output.append(f"{cor_lixo}{lixo}[/]")

        return "".join(final_output)

    def gerar_desafio(self, nivel: int) -> Tuple[str, str]:
        if not self.lexico: self.carregar_lexico()
        alvo = random.choice(self.lexico)
        visual_completo = ""

        # Nível 10+: Fragmentação com Iscas
        if nivel >= 10:
            iscas = random.sample([w for w in self.lexico if w != alvo], k=2)
            
            frag1 = iscas[0][:random.randint(3,5)]
            # Isca Esquerda (Phantom: Cinza / Void: Colorido)
            vis_trap1 = self.renderizar_palavra(frag1, nivel, is_target=False)
            
            # Alvo Central (Phantom: Neon Fragmentado / Void: Caos)
            vis_alvo = self.renderizar_palavra(alvo, nivel, is_target=True)
            
            frag2 = iscas[1][-random.randint(3,5):]
            # Isca Direita
            vis_trap2 = self.renderizar_palavra(frag2, nivel, is_target=False)
            
            sep = f"[dim]{self.sanitizar(random.choice(RUIDO_CHARS))}[/]"
            visual_completo = f"{vis_trap1}{sep} {vis_alvo} {sep}{vis_trap2}"
            
        else: 
            # Níveis 1-9: Apenas alvo com ruído
            str_base = alvo
            if nivel >= 4: str_base = str_base[::-1] # Espelho
            visual_completo = self.renderizar_palavra(str_base, nivel, is_target=True)

        return alvo, visual_completo

class ComplexySingularity:
    def scan_timeline(self, seed): return {"status": "SYNCED", "fib_val": 8, "t_offset": 300}
