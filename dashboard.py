import asyncio
import random
import time
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Log, Button, Label, Input, ProgressBar
from textual.screen import ModalScreen
from textual.reactive import reactive

# Imports
from src.classes.eremita import Eremita
from src.classes.reaper import Reaper
from src.classes.vampire import Vampire
from src.core.base import MinerEntity
from src.core.nexus import NexusEngine, ComplexySingularity
from src.core.rewards import RewardCalculator
from src.core.persistence import SaveManager

# --- GLOBAL MEMPOOL ---
class GlobalMempool:
    _pile = []
    @classmethod
    def add_failed_block(cls, level, bonus, streak):
        new = bonus + 0.05 if streak < 6 else bonus
        cls._pile.append({"level": level, "bonus": new})
        if len(cls._pile) > 50: cls._pile.pop(0)
    @classmethod
    def get_block(cls, lvl):
        for i, b in enumerate(cls._pile):
            if b["level"] == lvl: return cls._pile.pop(i)
        return {"level": lvl, "bonus": 0.0}

class Miner(MinerEntity):
    def calculate_mining_power(self): return 10.0
    def perform_cycle_action(self): return {}

# --- TELA DE INCINERAÇÃO (CORRIGIDA: BOTÃO SAIR) ---
class BurnModal(ModalScreen):
    CSS = """
    BurnModal { align: center middle; background: rgba(50, 0, 0, 0.95); }
    #burn_box { width: 80%; border: solid orange; background: #220500; padding: 1; }
    .fire-title { text-align: center; color: orange; text-style: bold; margin-bottom: 1; }
    .fire-info { text-align: center; color: #ff8888; margin-bottom: 1; }
    
    /* Botões lado a lado */
    #burn_btns { layout: grid; grid-size: 2; grid-gutter: 1; margin-top: 1; }
    """
    
    def compose(self):
        yield Container(
            Label("🔥 FORNALHA DE ENTROPIA", classes="fire-title"),
            Label("Sacrifique SNG para o Vazio.\nIsso purifica erros.", classes="fire-info"),
            Input(placeholder="Qtd a queimar...", type="number", id="burn_input"),
            
            # Botões de Ação e Saída
            Container(
                Button("RETORNAR", variant="primary", id="btn_close"),
                Button("INCINERAR", variant="error", id="btn_burn"),
                id="burn_btns"
            ),
            id="burn_box"
        )

    def on_button_pressed(self, event):
        if event.button.id == "btn_close":
            self.dismiss(0) # Sai sem queimar nada
            
        elif event.button.id == "btn_burn":
            try:
                val = float(self.query_one("#burn_input", Input).value)
                if val > 0: self.dismiss(val)
                else: self.dismiss(0)
            except:
                self.dismiss(0)

# --- SELETOR DE NÍVEL (COM BOTÃO SAIR) ---
class LevelSelectModal(ModalScreen):
    CSS = """
    LevelSelectModal { align: center middle; background: rgba(0,0,0,0.95); }
    #lvl_panel { width: 95%; border: solid green; background: #020502; padding: 1; }
    .title { text-align: center; color: green; text-style: bold; }
    #grid_levels { layout: grid; grid-size: 3; grid-gutter: 1; margin-top: 1; }
    Button { border: none; height: 1; }
    .t1 { background: #004400; color: #afa; }
    .t2 { background: #004444; color: #aff; }
    .t3 { background: #550000; color: #ffa; }
    .t4 { background: #330033; color: #f0f; }
    
    #btn_cancel { width: 100%; background: #333; color: #fff; margin-top: 1; }
    """
    def compose(self):
        yield Container(
            Label("🎛️ SELETOR DE FREQUÊNCIA", classes="title"),
            Grid(
                Button("NV 1", id="lvl_1", classes="t1"), Button("NV 2", id="lvl_2", classes="t1"), Button("NV 3", id="lvl_3", classes="t1"),
                Button("NV 4", id="lvl_4", classes="t1"), Button("NV 5", id="lvl_5", classes="t2"), Button("NV 6", id="lvl_6", classes="t2"),
                Button("NV 7", id="lvl_7", classes="t2"), Button("NV 8", id="lvl_8", classes="t2"), Button("NV 9", id="lvl_9", classes="t2"),
                Button("NV 10", id="lvl_10", classes="t3"), Button("NV 11", id="lvl_11", classes="t3"), Button("NV 12", id="lvl_12", classes="t3"),
                Button("NV 13", id="lvl_13", classes="t3"), Button("NV 14", id="lvl_14", classes="t4"), Button("NV 15", id="lvl_15", classes="t4"),
                Button("NV 16", id="lvl_16", classes="t4"), Button("NV 17", id="lvl_17", classes="t4"), Button("NV 18", id="lvl_18", classes="t4"),
                id="grid_levels"
            ),
            Button("CANCELAR SINTONIA", id="btn_cancel"),
            id="lvl_panel"
        )
    def on_button_pressed(self, event):
        if event.button.id == "btn_cancel": self.dismiss(0)
        elif "lvl_" in event.button.id: self.dismiss(int(event.button.id.split("_")[1]))

# --- TELA DO ENIGMA ---
class CodexModal(ModalScreen):
    CSS = """
    CodexModal { align: center middle; background: rgba(0,0,0,0.98); }
    #game_box { width: 95%; height: auto; padding: 1; margin: 1; }
    .visual { text-align: center; margin: 1; color: white; text-style: bold; background: #000; height: auto; }
    #timer_bar { width: 100%; color: yellow; margin-bottom: 1; }
    .theme-safe { border: solid green; background: #001100; }
    .theme-danger { border: heavy red; background: #220000; }
    .locked { opacity: 0.5; background: #330000; }
    .reward-info { text-align: center; color: gold; text-style: bold; border-bottom: dashed #444; padding-bottom: 1; margin-bottom: 1; width: 100%; }
    """
    
    def __init__(self, level: int, mode: str, pile_bonus: float = 0.0, reward_text: str = ""):
        super().__init__()
        self.engine = NexusEngine()
        self.level = level
        self.mode = mode
        self.pile_bonus = pile_bonus
        self.reward_text = reward_text
        self.target, self.visual = self.engine.gerar_desafio(level)
        self.total_time = 60 if level >= 10 else 30
        self.time_left = self.total_time
        self.is_locked = False

    def compose(self):
        theme = "theme-danger" if self.level >= 10 else "theme-safe"
        header = f"[bold white]PROTOCOL: {self.mode} // NVL: {self.level}[/]"
        if self.pile_bonus > 0: header += f" [bold yellow](+PILHA)[/]"
        reward_display = f"POTENCIAL:\n{self.reward_text.replace(' (', '\n(')}"

        yield Container(
            Label(header),
            Label(reward_display, classes="reward-info"),
            ProgressBar(total=self.total_time, show_eta=False, id="timer_bar"),
            Label(self.visual, classes="visual"), 
            Input(placeholder="DECODIFIQUE...", id="ans"),
            Button("VALIDAR HASH", id="btn", variant="warning"),
            Label("", id="status_msg"),
            id="game_box", classes=theme
        )

    def on_mount(self): self.set_interval(1.0, self.tick_timer)

    def tick_timer(self):
        self.time_left -= 1
        self.query_one("#timer_bar", ProgressBar).advance(1)
        if self.time_left <= 0: self.dismiss({"win": False, "reason": "TIMEOUT", "lvl": self.level})

    def on_button_pressed(self, event):
        if event.button.id == "btn" and not self.is_locked:
            ans = self.query_one("#ans", Input).value.strip().upper()
            if ans == self.target:
                elapsed = self.total_time - self.time_left
                self.dismiss({"win": True, "time": elapsed, "lvl": self.level, "bonus": self.pile_bonus})
            else:
                self.is_locked = True
                self.query_one("#ans", Input).disabled = True
                self.query_one("#btn", Button).disabled = True
                self.query_one("#game_box").add_class("locked")
                self.query_one("#status_msg", Label).update(f"[bold red]BLOQUEADO![/] Aguarde {self.time_left}s.")

# --- TELA QUÂNTICA ---
class QuantumLoading(ModalScreen):
    CSS = """QuantumLoading { align: center middle; background: black; } .info { color: cyan; text-align: center; margin-bottom: 1; text-style: bold; }"""
    def compose(self):
        yield Container(Label("🌌 INICIANDO PROTOCOLO QUÂNTICO...", id="status_lbl", classes="info"), ProgressBar(total=100, show_eta=False, id="bar"))
    def on_mount(self): self.run_worker(self.quantum_wait())
    async def quantum_wait(self):
        lbl = self.query_one("#status_lbl", Label)
        pbar = self.query_one("#bar", ProgressBar)
        msgs = ["Calibrando Qubits...", "Buscando Frequência...", "Medindo Entropia...", "Colapsando Onda..."]
        wait_time = random.randint(15, 90) / 10.0
        for msg in msgs:
            lbl.update(msg); pbar.advance(25); await asyncio.sleep(wait_time / 4)
        self.dismiss(random.random() < 0.3)

# --- DASHBOARD ---
class CloudProtocolApp(App):
    CSS = """
    Screen { background: #000; }
    #hud { height: 35%; border-bottom: solid #333; background: #0a0a0a; padding: 1; }
    #stats { width: 50%; padding: 1; border-right: solid #333; }
    #modes { width: 50%; align: center middle; padding: 1; }
    #bal { color: yellow; text-style: bold; }
    
    Button.mode-btn { width: 100%; margin-bottom: 1; border: none; }
    #btn_solo { background: #222; color: #ccc; border-left: solid green; }
    #btn_pit { background: #400; color: #fff; border-left: solid red; }
    #btn_quant { background: #006; color: #aaf; border-left: solid cyan; }
    #btn_burn { background: #d35400; color: #fff; border-left: solid orange; margin-top: 1; }
    
    #logs { height: 65%; }
    Log { background: #000; color: #0f0; border: none; overflow-x: hidden; }
    """
    sng_balance = reactive(0.0)
    error_streak = 0

    def __init__(self):
        super().__init__()
        self.wallet_id = "0xUser_Termux"
        loaded = SaveManager.load_game(self.wallet_id, "Miner")
        self.player = loaded if loaded else Miner(wallet_id=self.wallet_id, nickname="Neofito")

    def compose(self):
        yield Header(show_clock=True)
        with Horizontal(id="hud"):
            with Vertical(id="stats"):
                cls_name = self.player.__class__.__name__
                yield Label(f"[bold white]ID: {self.player.nickname}[/]")
                yield Label(f"[dim]CLASSE: {cls_name}[/]")
                yield Label("\n[bold yellow]SALDO (SNG):[/]")
                yield Label("0.0000", id="bal")
                yield Button("🔥 BURN (Sacrifício)", id="btn_burn", classes="mode-btn")
            with Vertical(id="modes"):
                yield Button("⛏️ SOLO (TREINO)", id="btn_solo", classes="mode-btn")
                yield Button("⚔️ THE PIT (ARENA)", id="btn_pit", classes="mode-btn")
                yield Button("🌌 QUANTUM ROOM", id="btn_quant", classes="mode-btn")
        with Vertical(id="logs"):
            yield Button("🧹 LIMPAR LOG", id="clean", variant="default")
            yield Log(id="console", highlight=True)
        yield Footer()

    def on_mount(self):
        self.sng_balance = self.player.get_balance()
        self.log_msg("[green]NEXUS v13.1 ONLINE. Travas de Segurança Removidas.[/]")

    def on_button_pressed(self, event):
        btn = event.button.id
        if btn == "clean": self.query_one("#console", Log).clear()
        elif btn == "btn_solo": self.push_screen(LevelSelectModal(), self.start_solo)
        elif btn == "btn_pit":
            if self.player.get_balance() < 20: self.log_msg("[red]⛔ Requer 20 SNG[/]"); return
            self.push_screen(CodexModal(level=11, mode="PIT", reward_text="50.0 SNG"), self.handle_pit)
        elif btn == "btn_quant": self.push_screen(QuantumLoading(), self.start_quant)
        elif btn == "btn_burn": self.push_screen(BurnModal(), self.handle_burn)

    def start_solo(self, level: int):
        if level > 0: # Só inicia se o nível for válido (não zero)
            block = GlobalMempool.get_block(level)
            rew_txt = RewardCalculator.estimate_potential(level, self.player.__class__.__name__, pile_bonus=block["bonus"])
            self.push_screen(CodexModal(level=level, mode="SOLO", pile_bonus=block["bonus"], reward_text=rew_txt), self.handle_solo)

    def start_quant(self, is_rift):
        mode, lvl = ("RIFT", 12) if is_rift else ("SAFE", 8)
        self.log_msg(f"[cyan]Estado: {mode}[/]")
        rew_txt = RewardCalculator.estimate_potential(lvl, self.player.__class__.__name__, is_rift=is_rift)
        self.push_screen(CodexModal(level=lvl, mode=mode, reward_text=rew_txt), self.handle_quant)

    def handle_solo(self, res):
        if res.get("win"):
            self.error_streak = 0
            calc = RewardCalculator.calculate(res["lvl"], res["time"], self.player.__class__.__name__, pile_bonus=res["bonus"])
            self.player.add_balance(calc["total"])
            self.log_msg(f"[green]✅ SUCESSO (Nv {res['lvl']})[/] +{calc['total']} SNG")
        else:
            self.error_streak += 1
            lvl = res.get("lvl", 1)
            GlobalMempool.add_failed_block(lvl, res.get("bonus", 0.0), self.error_streak)
            self.log_msg(f"[bold red]❌ FALHA.[/] Bloco retornado.")
        self.update_ui()

    def handle_pit(self, res):
        if res.get("win"): self.player.add_balance(50.0); self.log_msg("[bold yellow]🏆 VITÓRIA![/] +50.0 SNG")
        else: self.log_msg("[bold red]💀 ELIMINADO[/]")
        self.update_ui()

    def handle_quant(self, res):
        is_rift = "RIFT" in str(res)
        if res.get("win"):
            calc = RewardCalculator.calculate(12, res["time"], self.player.__class__.__name__, is_rift=is_rift)
            self.player.add_balance(calc["total"])
            self.log_msg(f"[bold cyan]🌌 SINTONIA![/] +{calc['total']} SNG")
        else: self.log_msg("[bold red]⚛️ COLAPSO[/]")
        self.update_ui()

    def handle_burn(self, amount):
        if amount > 0:
            if self.player.get_balance() >= amount:
                self.player.add_balance(-amount)
                self.error_streak = 0 
                self.log_msg(f"[bold orange]🔥 {amount:.4f} SNG INCINERADOS.[/]")
                self.log_msg("[dim]O Ciclo foi renovado.[/]")
            else:
                self.log_msg("[red]⛔ Saldo insuficiente.[/]")
        self.update_ui()

    def update_ui(self):
        self.sng_balance = self.player.get_balance()
        SaveManager.save_game(self.player)
    def watch_sng_balance(self, val): self.query_one("#bal", Label).update(f"{val:.4f}")
    def log_msg(self, msg): self.query_one("#console", Log).write_line(msg)

if __name__ == "__main__": app = CloudProtocolApp(); app.run()
