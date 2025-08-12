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
        # TODO: gerar e armazenar um ID usando uuid.uuid4()
        self.__id = uuid.uuid4()

    def get_id(self):
        # TODO: retornar o ID
        return self.__id

class AuditavelMixin:
    """Fornece logs simples ao console."""
    def log_evento(self, evento: str):
        # TODO: imprimir no formato  [LOG] <evento>
        print(f"[LOG] {evento}")

# -------------------------------------------------
# 3) Classe base Pessoa                           🡇
# -------------------------------------------------
class Pessoa:
    """Classe base para pessoas do sistema."""
    def __init__(self, nome: str, cpf: str):
        # TODO: armazenar nome e cpf como atributos protegidos
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        # TODO: retornar o nome
        return self._nome
    
    def __str__(self):
        # TODO: "Maria (123.456.789-00)"
        return f"{self.nome} {self._cpf}"

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
        # TODO: chamar super().__init__ e criar lista vazia de ingressos
        super().__init__(nome, cpf)
        self.__email = email
        self.__ingressos = []

    def comprar_ingresso(self, ingresso: Ingresso):
        # TODO: adicionar ingresso à lista
        if ingresso not in self.__ingressos:
            self.__ingressos.append(ingresso)
            return
        print(f"Cliente {self.nome} já possui ingresso {ingresso.codigo}.")

    def listar_ingressos(self):
        # TODO: imprimir os ingressos
        for ingresso in self.__ingressos: print(ingresso)
        

# -------------------------------------------------
# 6) Funcionario (herança múltipla + mixins)      🡇
# -------------------------------------------------
# TODO: Implementar a classe Funcionario
# - Herda de Pessoa, IdentificavelMixin e Logavel (pode usar AuditavelMixin)
# - Atributos: cargo, registro
# - Métodos:
#   • exibir_dados()    → imprime nome, cargo, registro e ID
#   • logar_entrada()   → registra no log
# -------------------------------------------------
class Funcionario(Pessoa, IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome:str, cpf:str, cargo:str, registro:str):
        IdentificavelMixin.__init__(self)
        Pessoa.__init__(self, nome, cpf)
        self.__cargo = cargo
        self.__registro = registro
    
    def exibir_dados(self):
        print(f"Nome: {self.nome}, Cargo: {self.__cargo}, Registro: {self.__registro}, ID: {self.get_id()}")

    def logar_entrada(self):
        self.log_evento(f"Funcionário {self._nome} com registro {self.__registro} foi criado.")

# -------------------------------------------------
# 7) Palco (objeto de composição)                 🡇
# -------------------------------------------------
#class Palco:
#    """Objeto que compõe o Festival."""
#    def __init__(self, nome: str, capacidade: int):
#        self.nome = nome
#        self.capacidade = capacidade
#
#    def resumo(self):
#        # TODO: retornar string "Palco X – cap. Y pessoas"
#        return f"Palco {self.nome} - cap {self.capacidade} pessoas"

# -------------------------------------------------
# 8) Festival (composição com Palco)              🡇
# -------------------------------------------------
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
class Festival:
    class Palco:
        """Objeto que compõe o Festival."""
        def __init__(self, nome: str, capacidade: int):
            self.nome = nome
            self.capacidade = capacidade

        def resumo(self):
            # TODO: retornar string "Palco X – cap. Y pessoas"
            return f"Palco {self.nome} - cap {self.capacidade} pessoas"
        
    def __init__(self, nome:str, data:date, local:str, nomePalco:str, capacidadePalco:int):
        self.nome = nome
        self.data = data
        self.local = local
        self.palco = self.Palco(nomePalco, capacidadePalco)
        self.clientes = []
        self.equipe = []
        self.ingressos = []
    
    def vender_ingresso(self, cliente, ingresso):
        if len(self.ingressos) >= self.palco.capacidade: 
            print("Ingressos esgotados!")
            return
        
        if ingresso in self.ingressos: return
        self.ingressos.append(ingresso)

        if cliente not in self.clientes: self.clientes.append(cliente)
        cliente.comprar_ingresso(ingresso)

        print(f"Ingresso {ingresso.codigo} vendido para {cliente._nome}.")
        return True

    def adicionar_funcionario(self, funcionario:Funcionario):
        if funcionario in self.equipe: return
        self.equipe.append(funcionario)

    def listar_clientes(self):
        print("Clientes:")
        for cliente in self.clientes:
            print(f"- {cliente.nome}")  

    def listar_equipe(self):
        print("Equipe:")
        for funcionario in self.equipe:
            print(f" - {funcionario.nome}") 

    def listar_ingressos(self):        
        print("Ingressos:")
        for ingresso in self.ingressos:
            print(f" - {ingresso}")   

# -------------------------------------------------
# 9) EmpresaEventos                               🡇
# -------------------------------------------------
class EmpresaEventos:
    """Agrupa seus festivais (has‑a)."""
    def __init__(self, nome: str):
        # TODO: validar nome (≥ 3 letras) e criar lista vazia de festivais
        if len(nome.strip()) < 3: raise ValueError("O nome da empresa deve ter no mínimo 3 letras.")

        self.__nome = nome
        self.__festivais = []

    @property
    def nome(self):
        # TODO: retornar nome
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        # TODO: validar + atualizar nome
        if len(novo_nome.strip()) < 3: raise ValueError("O nome da empresa deve ter no mínimo 3 letras.")

        self.__nome = novo_nome

    def adicionar_festival(self, festival):
        # TODO: adicionar festival à lista
        if festival not in self.__festivais: self.__festivais.append(festival)

    def buscar_festival(self, nome: str):
        # TODO: retornar festival ou None
        for festival in self.__festivais:
            if nome.strip().lower() == festival.nome.strip().lower():
                return festival
        return None

    def listar_festivais(self):
        # TODO: imprimir todos os festivais
        if not self.__festivais:
            print("Nenhum festival cadastrado.")
            return
        
        print(f"Festivais da empresa '{self.nome}':")
        for festival in self.__festivais:
            print(f"- {festival.nome} ({festival.data} - {festival.local})")

# -------------------------------------------------
# 10) Auditor (Identificável + Logável)           🡇
# -------------------------------------------------
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
class Auditor(IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def logar_entrada(self):
        return self.log_evento(f"Auditor {self.nome} entrou no sistema.")

    def auditar_festival(self, festival:Festival):
        if festival.palco.capacidade >= len(festival.clientes) and len(festival.equipe) >= 1:
            print(f"Festival '{festival.nome}' está em conformidade.")
            return
        print(f"Festival '{festival.nome}' apresenta não conformidades.")

    def __str__(self):
        return f"Auditor {self.nome} (ID: {self.get_id()})"   
