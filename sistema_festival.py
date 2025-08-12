from abc import ABC, abstractmethod
import uuid
from datetime import date

# -------------------------------------------------
# 1) Interface                                    🡇
# -------------------------------------------------
class Logavel(ABC):
    """Qualquer classe logável DEVE implementar logar_entrada()."""
    @abstractmethod
    def logar_entrada(self):
        pass

# -------------------------------------------------
# 2) Mixins                                       🡇
# -------------------------------------------------
class IdentificavelMixin:
    """Gera um ID único; combine‑o com outras classes."""
    def __init__(self):
        self.id = self.get_id()
        
    def get_id(self):
        return uuid.uuid4()

class AuditavelMixin:
    """Fornece logs simples ao console."""
    def log_evento(self, evento: str):
        print(f"[LOG] {evento}")
        pass

# -------------------------------------------------
# 3) Classe base Pessoa                           🡇
# -------------------------------------------------
class Pessoa:
    """Classe base para pessoas do sistema."""
    def __init__(self, nome: str, cpf: str):
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome
    def __str__(self):
        return f"{self._nome} - {self._cpf}"
        

# -------------------------------------------------
# 4) Ingresso — classe simples                    🡇
# -------------------------------------------------
class Ingresso:
    def __init__(self, codigo: str, tipo: str, preco: float):
        self.codigo = codigo
        self.tipo = tipo  # ex.: 'Pista', 'VIP', 'Backstage'
        self.preco = preco
    def __str__(self):
        return f"[{self.codigo}] {self.tipo} – R$ {self.preco:.2f}"

# -------------------------------------------------
# 5) Cliente                                      🡇
# -------------------------------------------------
class Cliente(Pessoa):
    """Herda de Pessoa e possui ingressos."""
    def __init__(self, nome: str, cpf: str, email: str):
        super().__init__(nome, cpf)
        self._email = email
        self._ingressos = []
        
    def comprar_ingresso(self, ingresso: Ingresso):
        self._ingressos.append(ingresso)
    def listar_ingressos(self):
        for ing in self._ingressos:
            print(ing)

# -------------------------------------------------
# 6) Funcionario (herança múltipla + mixins)      🡇
# -------------------------------------------------
class Funcionario(Pessoa, IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome, cpf, cargo: str, registro: str):
        super().__init__(nome, cpf)
        self._cargo = cargo
        self._registro = registro

    def exibir_dados(self):
        print(f"Nome: {self._nome} - Cargo: {self._cargo}")    

    def logar_entrada(self):
        self.log_evento(f"Funcionário {self._nome} com registro {self._registro} foi criado.")
           

# TODO: Implementar a classe Funcionario
# - Herda de Pessoa, IdentificavelMixin e Logavel (pode usar AuditavelMixin)
# - Atributos: cargo, registro
# - Métodos:
#   • exibir_dados()    → imprime nome, cargo, registro e ID
#   • logar_entrada()   → registra no log

# -------------------------------------------------
# 7) Palco (objeto de composição)                 🡇
# -------------------------------------------------

        
# -------------------------------------------------
# 8) Festival (composição com Palco)              🡇
# -------------------------------------------------
class Festival():
    class Palco:
        """Objeto que compõe o Festival."""
        def __init__(self, nome: str, capacidade: int):
            self.nome = nome
            self.capacidade = capacidade
        
        def resumo(self):
            return f"Palco {self.nome} - cap {self.capacidade} pessoas"
    def __init__(self, nome:str, data:date, local:str, nomePalco: str, capacidadePalco: str):
        self.nome = nome
        self.data = data
        self.local = local
        self.clientes = []
        self.equipe = []
        self.ingressos = []
        self.palco = self.Palco(nomePalco, capacidadePalco)

    def vender_ingresso(self, cliente, ingresso):
        if len(self.ingressos) >= self.palco.capacidade:
            print("Ingressos esgotados!")
            return False
    
    
        for ing in cliente._ingressos:
            if ing.codigo == ingresso.codigo:
                print(f"Cliente {cliente._nome} já possui ingresso {ingresso.codigo}.")
                return False

        if cliente not in self.clientes:
            self.clientes.append(cliente)
        self.ingressos.append(ingresso)
        cliente.comprar_ingresso(ingresso)
        print(f"Ingresso {ingresso.codigo} vendido para {cliente._nome}.")
        return True

    def adicionar_funcionario(self, func):
        if func in self.equipe:
            print(f"Funcionário {func._nome} já está na equipe.")

        else:
            self.equipe.append(func)    
            print(f"Funcionário {func._nome} adicionado à equipe.")

    def listar_clientes(self):
        print("Clientes:")
        for cliente in self.clientes:
            print(f"- {cliente._nome}")  

    def listar_equipe(self):
        print("Equipe:")
        for func in self.equipe:
            print(f" - {func._nome}") 

    def listar_ingressos(self):        
        print("Ingressos:")
        for ing in self.ingressos:
            print(f" - {ing}")             

# TODO: Implementar a classe Festival
# - Atributos: nome, data, local, palco
# - Listas: clientes, equipe, ingressos
# - Métodos:
#   • vender_ingresso(cliente, ingresso)  (checar duplicidade & capacidade)
#   • adicionar_funcionario(func)
#   • listar_clientes()
#   • listar_equipe()
#   • listar_ingressos()

# -------------------------------------------------
# 9) EmpresaEventos                               🡇
# -------------------------------------------------
class EmpresaEventos:
    """Agrupa seus festivais (has‑a)."""
    def __init__(self, nome: str):
        if len(nome.strip()) < 3:
            raise ValueError("O nome da empresa deve ter no mínimo 3 letras.")
        # TODO: validar nome (≥ 3 letras) e criar lista vazia de festivais
        self._nome = nome
        self._festivais = []

    @property
    def nome(self):
        return self._nome
        
    @nome.setter
    def nome(self, novo_nome: str):
        if len(novo_nome.strip()) < 3:
            raise ValueError("O nome da empresa deve ter no mínimo 3 letras.")
        
        else:
            self._nome = novo_nome
        # TODO: validar + atualizar nome
        
    def adicionar_festival(self, festival):
        self._festivais.append(festival)
        # TODO: adicionar festival à lista
        
    def buscar_festival(self, nome: str):
        for f in self._festivais:
            if f.nome.lower() == nome.lower():
                return f
        return None

        # TODO: retornar festival ou None
        
    def listar_festivais(self):
        if not self._festivais:
            print("Nenhum festival cadastrado.")
        else:
            print(f"Festivais da empresa '{self._nome}':")
            for f in self._festivais:
                print(f"- {f.nome} ({f.data} - {f.local})")
        # TODO: imprimir todos os festivais

# -------------------------------------------------
# 10) Auditor (Identificável + Logável)           🡇
# -------------------------------------------------
class Auditor(IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def logar_entrada(self):
        self.log_evento(f"Auditor {self.nome} entrou no sistema.")

    def auditar_festival(self, fest):
        conformidade = True

        if len(fest.clientes) > fest.palco.capacidade:
            print("Falha: número de clientes excede a capacidade do palco.")
            conformidade = False 

        else:
            print("Número de clientes dentro da capacidade.")     

        if len(fest.equipe) < 1:
            print("Falha: festival não possui funcionários.")
            conformidade = False
        else:
            print("Festival possui equipe.")

        if conformidade:
            print(f"Festival '{fest.nome}' está em conformidade.")
        else:
            print(f"Festival '{fest.nome}' apresenta não conformidades.")    
    def __str__(self):
        return f"Auditor {self.nome} (ID: {self.id})"   
         
# TODO: Implementar a classe Auditor
# - Herda de IdentificavelMixin e Logavel
# - Atributo: nome
# - Métodos:
#   • logar_entrada() → registra entrada no sistema
#   • auditar_festival(fest) → verifica:
#         ▸ Nº de clientes ≤ capacidade do palco
#         ▸ existe ao menos 1 funcionário
#     imprime relatório de conformidade
#   • __str__() → "Auditor <nome> (ID: ...)"

# -------------------------------------------------
# 11) Bloco de teste                              🡇
# -------------------------------------------------
if __name__ == "__main__": 

     # Criar empresa
    empresa = EmpresaEventos("Mega Eventos LTDA")

    # Criar dois festivais
    fest1 = Festival(
        nome="Mossoró Cidade Junina",
        data=date(2025, 12, 5),
        local="Mossoró",
        nomePalco="Palco Principal",
        capacidadePalco=3
    )

    fest2 = Festival(
        nome="Finecap",
        data=date(2025, 11, 20),
        local="Pau dos Ferros",
        nomePalco="Palco da Praça",
        capacidadePalco=2
    )

    # Adicionar festivais à empresa
    empresa.adicionar_festival(fest1)
    empresa.adicionar_festival(fest2)

    # Criar clientes
    c1 = Cliente("Ana", "111.111.111-11", "ana@email.com")
    c2 = Cliente("Bruno", "222.222.222-22", "bruno@email.com")
    c3 = Cliente("Carlos", "333.333.333-33", "carlos@email.com")

    # Criar ingressos
    ing1 = Ingresso("001", "Pista", 100.0)
    ing2 = Ingresso("002", "VIP", 200.0)
    ing3 = Ingresso("003", "Backstage", 500.0)

    # Criar funcionários
    f1 = Funcionario("Daniel", "444.444.444-44", "Segurança", "S001")
    f2 = Funcionario("Eduarda", "555.555.555-55", "Produtora", "P002")

    # Adicionar funcionários aos festivais
    fest1.adicionar_funcionario(f1)
    fest1.adicionar_funcionario(f2)
    fest2.adicionar_funcionario(f2)

    # Vender ingressos
    fest1.vender_ingresso(c1, ing1)
    fest1.vender_ingresso(c2, ing2)
    fest1.vender_ingresso(c3, ing3)

    # Tentativa de exceder capacidade
    fest1.vender_ingresso(c1, Ingresso("004", "Extra", 50.0))

    # Listar participantes e ingressos
    fest1.listar_clientes()
    fest1.listar_equipe()
    fest1.listar_ingressos()

    # Criar auditor
    auditor = Auditor("Fernanda")
    auditor.logar_entrada()

    # Auditar festivais
    print("\nAuditoria Festival 1:")
    auditor.auditar_festival(fest1)

    print("\nAuditoria Festival 2:")
    auditor.auditar_festival(fest2)

    # Listar festivais da empresa
    empresa.listar_festivais()

    """
    TODO:
      • Crie 1 empresa, 2 festivais, clientes, equipe e auditor.
      • Venda ingressos, liste participantes, audite festivais.
      • Mostre saídas no console para validar implementações.
    """
    pass

