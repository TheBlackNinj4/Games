import os
import random
import json
import time

class projeto():
    def __init__ (self, nome_sistema):
        self._nome_sistema = nome_sistema
        # Esta é a lista que centraliza tudo:
        self.projetos_cadastrados = [] 
        self.carregar_jogo()
        
    def salvar(self):
            # Salvamos a lista inteira de projetos
        with open("banco_de_dados.json", "w") as f:
            json.dump(self.projetos_cadastrados, f, indent=4)
    
    def limpar_tela(self):
        time.sleep(1.9)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.salvar()
    
    def carregar_jogo(self):
        if os.path.exists("banco_de_dados.json"):
            with open("banco_de_dados.json", "r") as f:
                self.projetos_cadastrados = json.load(f)
        
    def cadastrar(self):
        self.limpar_tela()
        nome = input("Digite o nome do cliente: ")
        try:
            valor = float(input("Digite o valor: "))
            codigo = random.randint(1000, 9999) # Gera um código aleatório
            rota = input("Selecione a rota: Roxo, Azul ou Verde: ").capitalize()
            
            # Cria um dicionário com os dados
            novo_projeto = {
                "nome": nome,
                "valor": valor,
                "codigo": codigo,
                "rota": rota
            }
            
            # Adiciona na sua lista (o "banco de dados" temporário)
            self.projetos_cadastrados.append(novo_projeto)
            print(f"Sucesso! Código gerado: {codigo}")
            
        except ValueError:
            print("Erro: No campo 'valor', digite apenas números e use ponto para centavos.")
            
    def pesquisar(self):
        self.limpar_tela()
        print(f"Total de clientes no sistema: {len(self.projetos_cadastrados)}")
        
        busca = input("Digite parte do nome ou código: ").lower()
        encontrados_nesta_busca = 0

        for p in self.projetos_cadastrados:
            if busca in p['nome'].lower() or busca == str(p['codigo']):
                print(f"\n[{p['codigo']}] - {p['nome']} | Valor: R${p['valor']} | Rota: {p['rota']}")
                encontrados_nesta_busca += 1
        
        print(f"\nForam encontrados {encontrados_nesta_busca} resultados.")
        if encontrados_nesta_busca == 0:
            print("Nenhum registro condiz com a busca.")
            
    def executar(self):
        self.limpar_tela()
        while True:
            print("1. Cadastrar | 2. Pesquisar | 3.  | 4. Sair")
            op = input("Opção: ")
            if op == "1": self.cadastrar()
            elif op == "2": self.pesquisar()
            elif op == "3": pass
            elif op == "4": break
        
meu_sistema = projeto("Sistema")

meu_sistema.executar()
