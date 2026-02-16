import time
import os
import json

CORES = {
    'limpar': '\033[0m',
    'verde': '\033[92m',
    'vermelho': '\033[91m',
    'ciano': '\033[96m'
}

class Livro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True
        
    def __str__(self):
        status = f"{CORES['verde']}Disponível{CORES['limpar']}" if self.disponivel else f"{CORES['vermelho']}Emprestado{CORES['limpar']}"
        return f"{self.titulo} | Autor: {self.autor} | [{status}]"

class Biblioteca:
    def __init__(self):
        self.acervo = []
        self.carregar_dados() # Carrega ao iniciar

    def carregar_dados(self):
        try:
            with open("biblioteca_save.json", "r", encoding='utf-8') as f:
                dados = json.load(f)
                self.acervo = [] # Limpa o acervo atual para não duplicar
                for item in dados:
                    novo = Livro(item['titulo'], item['autor'])
                    novo.disponivel = item['disponivel']
                    self.acervo.append(novo)
        except FileNotFoundError:
            pass # Se não existir o arquivo, ignora e começa vazio

    
    def salvar(self):
        dados = []
        for livro in self.acervo:
            dados.append({
                "titulo": livro.titulo,
                "autor": livro.autor,
                "disponivel": livro.disponivel
            })
        
        with open("biblioteca_save.json", "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"\n{CORES['verde']}Progresso salvo com sucesso!{CORES['limpar']}")

    def limpar_tela(self):
        input(f"\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

    def adicionar_livro(self, titulo, autor):
        novo_livro = Livro(titulo, autor)
        self.acervo.append(novo_livro)
        print(f"Livro '{titulo}' adicionado!")

    def listar_livros(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{CORES['ciano']}--- ACERVO DA BIBLIOTECA ---{CORES['limpar']}")
            
            if not self.acervo:
                print("A Biblioteca está vazia.")
                self.limpar_tela()
                return

            # Exibe todos os livros inicialmente
            for livro in self.acervo:
                print(livro)

            print("\n" + "-"*30)
            busca = input(f"Digite para pesquisar ({CORES['verde']}Título ou Autor{CORES['limpar']}) ou pressione {CORES['vermelho']}Enter{CORES['limpar']} para voltar: ").strip().lower()

            if not busca:
                break  # Sai do loop e volta para o menu principal

            # Lógica de Filtro: Procura a 'busca' dentro do título ou do autor
            resultados = [
                livro for livro in self.acervo 
                if busca in livro.titulo.lower() or busca in livro.autor.lower()
            ]

            # Exibe os resultados da pesquisa
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{CORES['ciano']}--- RESULTADOS PARA: '{busca}' ---{CORES['limpar']}")
            if resultados:
                for res in resultados:
                    print(res)
            else:
                print(f"{CORES['vermelho']}Nenhum livro ou autor encontrado.{CORES['limpar']}")
            
            input(f"\nPressione Enter para pesquisar novamente...")
        
    def emprestar_livro(self, titulo_busca):
        for livro in self.acervo:
            if livro.titulo.lower() == titulo_busca.lower():
                if livro.disponivel:
                    livro.disponivel = False
                    print(f"Sucesso! Você pegou '{livro.titulo}'.")
                else:
                    print("Este livro já está emprestado.")
                self.limpar_tela()
                return
        print("Livro não encontrado.")
        self.limpar_tela()

    def devolver_livro(self, titulo_busca):
        for livro in self.acervo:
            if livro.titulo.lower() == titulo_busca.lower():
                if not livro.disponivel: # Se NÃO está disponível, pode devolver
                    livro.disponivel = True
                    print(f"Obrigado! '{livro.titulo}' foi devolvido.")
                else:
                    print("Este livro já consta na prateleira.")
                self.limpar_tela()
                return
        print("Livro não encontrado.")
        self.limpar_tela()
    
    def executar(self):
        self.limpar_tela
        while True:
            print("="*40)
            print(f"{CORES['verde']}SISTEMA DE BIBLIOTECA{CORES['limpar']}")
            print("="*40)
            print("1. Adicionar Livro\n2. Listar Livros\n3. Emprestar Livro\n4. Devolver Livro\n5. Sair")
            
            op = input("\nEscolha uma opção: ")

            if op == "1":
                t = input("Título: ")
                a = input("Autor: ")
                self.adicionar_livro(t, a)
            elif op == "2":
                self.listar_livros()
            elif op == "3":
                t = input("Título para empréstimo: ")
                self.emprestar_livro(t)
            elif op == "4":
                t = input("Título para devolução: ")
                self.devolver_livro(t)
            elif op == "5":
                self.salvar()
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

# Iniciar o sistema
minha_biblioteca = Biblioteca()
minha_biblioteca.executar()

[
    {
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J.K. Rowling",
        "disponivel": true
    },
    {
        "titulo": "Harry Potter e a Câmara Secreta",
        "autor": "J.K. Rowling",
        "disponivel": true
    },
    {
        "titulo": "Harry Potter e o Prisioneiro de Azkaban",
        "autor": "J.K. Rowling",
        "disponivel": true
    },
    {
        "titulo": "Harry Potter e a Ordem da Fênix",
        "autor": "J.K. Rowling",
        "disponivel": false
    },
    {
        "titulo": "Harry Potter e o Enigma do Príncipe",
        "autor": "J.K. Rowling",
        "disponivel": true
    },
    {
        "titulo": "Harry Potter e as Relíquias da Morte",
        "autor": "J.K. Rowling",
        "disponivel": false
    },
    {
        "titulo": "Harry Potter e a Criança Amaldiçoada",
        "autor": "J.K. Rowling",
        "disponivel": true
    }
]
