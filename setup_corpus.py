import urllib.request
import os

# 1. Lista Temática (A Alma do Jogo)
TEMAS_CORE = [
    "SINGULARIDADE", "CRIPTOGRAFIA", "BLOCKCHAIN", "ETHEREUM", "BITCOIN", "SATOSHI",
    "FIBONACCI", "AUREA", "FRACTAL", "QUANTICO", "ENTROPIA", "SINTROPIA",
    "EREMITA", "CEIFADOR", "VAMPIRO", "ARQUITETO", "MATRIX", "ORACULO",
    "NEUROPLASTICIDADE", "DOPAMINA", "SEROTONINA", "CORTEX", "SINAPSE",
    "ALGORITMO", "HEURISTICA", "RECURSIVIDADE", "POLIMORFISMO", "HERANÇA",
    "PYTHON", "LINUX", "TERMUX", "KERNEL", "SHELL", "BASH", "ROOT",
    "LATENCIA", "PING", "PACKET", "SOCKET", "HANDSHAKE", "FIREWALL",
    "DESCENTRALIZADO", "DISTRIBUIDO", "CONSENSO", "VALIDACAO", "PROOF",
    "WORK", "STAKE", "AUTHORITY", "HISTORY", "TIME", "SPACE", "REALITY"
]

# 2. URL de um dicionário PT-BR limpo (Palavras comuns)
# Usando uma lista da USP (IME) ou similar raw do GitHub
URL_DICIONARIO = "https://raw.githubusercontent.com/python-probr/palavras/master/palavras.txt"

def gerar_corpus():
    print("--- GERADOR DE CORPUS DO CAOS ---")
    palavras_finais = set(TEMAS_CORE) # Set evita duplicatas
    
    # Tenta baixar o dicionário da internet
    try:
        print(f"Baixando dicionário de {URL_DICIONARIO}...")
        with urllib.request.urlopen(URL_DICIONARIO) as response:
            texto = response.read().decode('utf-8')
            lista_web = texto.splitlines()
            
            # Filtra palavras pequenas ou inúteis
            count = 0
            for p in lista_web:
                p_limpa = p.strip().upper()
                if len(p_limpa) >= 5 and p_limpa.isalpha():
                    palavras_finais.add(p_limpa)
                    count += 1
            print(f"Sucesso! {count} palavras baixadas da rede.")
            
    except Exception as e:
        print(f"⚠️ Sem internet ou erro no download: {e}")
        print("Gerando corpus apenas com palavras temáticas.")

    # Salva no arquivo
    with open("corpus_caos.txt", "w", encoding="utf-8") as f:
        for p in sorted(list(palavras_finais)):
            f.write(p + "\n")
            
    print(f"\n✅ 'corpus_caos.txt' criado com {len(palavras_finais)} palavras.")
    print("O Nexus agora tem munição pesada.")

if __name__ == "__main__":
    gerar_corpus()
