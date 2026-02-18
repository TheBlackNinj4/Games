import os
import json
import pygame

class Jogo():
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Clicker Profissional")
        self.relogio = pygame.time.Clock()
        self.ingame = True
        
        self.moedas = 0
        self.moedas_por_segundo = 0
        self.multiplicador_cliques = 1
        self.fonte = pygame.font.SysFont("Arial", 25, bold=True)
        self.fonte_particula = pygame.font.SysFont("Arial", 20, bold=True)
        self.ultimo_tempo = pygame.time.get_ticks()
        
        self.particulas = []
        self.carregar_assets()

        self.compras = [
            {"nome": "Cursor", "custo": 10, "ganho": 1, "rect": pygame.Rect(10, 100, 250, 50)},
            {"nome": "Fazenda", "custo": 100, "ganho": 10, "rect": pygame.Rect(10, 160, 250, 50)},
            {"nome": "Templo", "custo": 500, "ganho": 100, "rect": pygame.Rect(10, 220, 250, 50)}
        ]
        
        self.upgrades = [
            {"nome": "Mouse", "custo": 600, "ganho": 5, "rect": pygame.Rect(0, 0, 0, 0)},
            {"nome": "Cursor", "custo": 1000, "ganho": 2, "rect": pygame.Rect(0, 0, 0, 0)},
            {"nome": "Fazenda", "custo": 1000, "ganho": 2, "rect": pygame.Rect(0, 0, 0, 0)},
            {"nome": "Templo", "custo": 5000, "ganho": 2, "rect": pygame.Rect(0, 0, 0, 0)}
        ]
        
        self.carregar()
        self.recalcular_mps()

    def carregar_assets(self):
        self.img_fundo = None
        self.img_botao_compra = None
        self.img_botao_upgrade = None

        try:
            self.img_fundo = pygame.image.load(os.path.join(os.path.dirname(__file__), "fundo.png")).convert()
            self.img_botao_compra = pygame.image.load(os.path.join(os.path.dirname(__file__), "botao_loja.png")).convert_alpha()
            self.img_botao_upgrade = pygame.image.load(os.path.join(os.path.dirname(__file__), "botao_upgrade.png")).convert_alpha()
        except:
            print("Imagens não encontradas. Usando cores sólidas.")

    def criar_particula(self, x, y, texto, cor=(255, 255, 0)):
        self.particulas.append({
            "x": x,
            "y": y,
            "texto": texto,
            "vida": 40,
            "cor": cor
        })

    def recalcular_mps(self):
        soma = 0
        for item in self.compras:
            if item["custo"] > 10 or item["nome"] != "Cursor":
                soma += item["ganho"]
        self.moedas_por_segundo = soma

    def salvar(self):
        caminho = os.path.join(os.path.dirname(__file__), "savegame.json")
        dados = {
            "moedas": self.moedas,
            "mps": self.moedas_por_segundo,
            "cliques": self.multiplicador_cliques,
            "custos_compras": [item["custo"] for item in self.compras],
            "ganhos_compras": [item["ganho"] for item in self.compras],
            "upgrades_restantes": [{"nome": u["nome"], "custo": u["custo"], "ganho": u["ganho"]} for u in self.upgrades]
        }
        with open(caminho, "w") as f:
            json.dump(dados, f)

    def carregar(self):
        caminho = os.path.join(os.path.dirname(__file__), "savegame.json")
        if os.path.exists(caminho):
            with open(caminho, "r") as f:
                dados = json.load(f)
                self.moedas = dados.get("moedas", 0)
                self.moedas_por_segundo = dados.get("mps", 0)
                self.multiplicador_cliques = dados.get("cliques", 1)
                
                for i, custo in enumerate(dados.get("custos_compras", [])):
                    if i < len(self.compras):
                        self.compras[i]["custo"] = custo
                        self.compras[i]["ganho"] = dados["ganhos_compras"][i]

                nomes_vivos = [u["nome"] for u in dados.get("upgrades_restantes", [])]
                self.upgrades = [u for u in self.upgrades if u["nome"] in nomes_vivos]

    def loop_game(self):
        while self.ingame:
            if self.img_fundo:
                self.tela.blit(self.img_fundo, (0, 0))
            else:
                self.tela.fill((30, 30, 30))

            tempo_agora = pygame.time.get_ticks()
            teste = tempo_agora - self.ultimo_tempo
            if teste >= 1000:
                self.moedas += self.moedas_por_segundo
                self.ultimo_tempo = tempo_agora
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salvar()
                    self.ingame = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    clicou_botao = False

                    for item in self.compras:
                        if item["rect"].collidepoint(evento.pos):
                            clicou_botao = True
                            if self.moedas >= item["custo"]:
                                self.moedas -= item["custo"]
                                self.moedas_por_segundo += item["ganho"]
                                item["custo"] = int(item["custo"] * 1.5)
                                self.criar_particula(evento.pos[0], evento.pos[1], f"-${item['custo']}", (255, 50, 50))
                                self.salvar()

                    upgrade_para_remover = None
                    for i, up in enumerate(self.upgrades):
                        if up["rect"].collidepoint(evento.pos):
                            clicou_botao = True
                            if self.moedas >= up["custo"]:
                                self.moedas -= up["custo"]
                                if up["nome"] == "Mouse":
                                    self.multiplicador_cliques += up["ganho"]
                                else:
                                    for compra in self.compras:
                                        if compra["nome"] == up["nome"]:
                                            compra["ganho"] *= up["ganho"]
                                self.recalcular_mps()
                                upgrade_para_remover = i
                                self.criar_particula(evento.pos[0], evento.pos[1], "UPGRADE!", (50, 255, 50))
                                self.salvar()

                    if upgrade_para_remover is not None:
                        self.upgrades.pop(upgrade_para_remover)

                    if not clicou_botao:
                        valor_ganho = 1 * self.multiplicador_cliques
                        self.moedas += valor_ganho
                        self.criar_particula(evento.pos[0], evento.pos[1], f"+{valor_ganho}")

            pygame.draw.rect(self.tela, (0, 0, 0, 150), (0, 0, 800, 85))
            txt_moedas = self.fonte.render(f"MOEDAS: {int(self.moedas)}", True, (255, 215, 0))
            txt_mps = self.fonte.render(f"FPS: {self.moedas_por_segundo} | CLIQUE: x{self.multiplicador_cliques}", True, (200, 200, 200))
            self.tela.blit(txt_moedas, (20, 10))
            self.tela.blit(txt_mps, (20, 45))

            for item in self.compras:
                if self.img_botao_compra:
                    self.tela.blit(self.img_botao_compra, (item["rect"].x, item["rect"].y))
                else:
                    cor = (50, 50, 50) if self.moedas < item["custo"] else (0, 150, 0)
                    pygame.draw.rect(self.tela, cor, item["rect"], border_radius=8)
                
                txt = self.fonte.render(f"{item['nome']}: ${item['custo']}", True, (255, 255, 255))
                self.tela.blit(txt, (item["rect"].x + 15, item["rect"].y + 12))

            for i, up in enumerate(self.upgrades):
                up["rect"] = pygame.Rect(520, 100 + (i * 65), 250, 50)
                if self.img_botao_upgrade:
                    self.tela.blit(self.img_botao_upgrade, (up["rect"].x, up["rect"].y))
                else:
                    cor = (50, 50, 50) if self.moedas < up["custo"] else (200, 150, 0)
                    pygame.draw.rect(self.tela, cor, up["rect"], border_radius=8)
                
                txt = self.fonte.render(f"UP {up['nome']}: ${up['custo']}", True, (255, 255, 255))
                self.tela.blit(txt, (up["rect"].x + 15, up["rect"].y + 12))

            for particula in self.particulas[:]:
                txt_part = self.fonte_particula.render(particula["texto"], True, particula["cor"])
                self.tela.blit(txt_part, (particula["x"], particula["y"]))
                particula["y"] -= 2
                particula["vida"] -= 1
                if particula["vida"] <= 0:
                    self.particulas.remove(particula)

            pygame.display.update()
            self.relogio.tick(60)

if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.loop_game()