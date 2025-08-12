from abc import ABC, abstractmethod
import uuid
from datetime import date
from extra_minxin import Relatorio,excluir_arquivo

#const
ARQUIVO_RELATORIO = './relatorio.txt'
excluir_arquivo(ARQUIVO_RELATORIO)

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
class Cliente(Pessoa,):
    __clientes = []
    
    """Herda de Pessoa e possui ingressos."""
    def __init__(self, nome: str, cpf: str, email: str):
        super().__init__(nome, cpf)
        self._email = email
        self._ingressos = []
        self.__clientes.append(self)
        
    def comprar_ingresso(self, ingresso: Ingresso):
        self._ingressos.append(ingresso)
        
    def gerar_relatorio_ingressos(self):
        ingressos_lista = []
        linha_relatorio = f'Clienete : {self.nome}, ingressos :'
        for ingresso in self._ingressos: ingressos_lista.append(ingresso.codigo)
        if ingressos_lista:
            for ingresso in ingressos_lista: linha_relatorio+= f' {ingresso}'
        else:
            linha_relatorio += ' Nenhum ingresso comprado'
            
        return linha_relatorio


    @classmethod
    def gerar_relatorio_ingresos_geral(cls):
        """gera o relatorio de ingressos de todos os clientes"""
        conteudo = str()
        for objeto in cls.__clientes:
            conteudo+=f'{objeto.gerar_relatorio_ingressos()}\n'
        
        editor_arquivo = Relatorio(ARQUIVO_RELATORIO)
        
        editor_arquivo.rescrever_arquivo(conteudo)
        

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
class Palco:
    """Objeto que compõe o Festival."""
    def __init__(self, nome: str, capacidade: int):
        self.nome = nome
        self.capacidade = capacidade
    
    def resumo(self):
        return f"Palco {self.nome} - cap {self.capacidade} pessoas"
        
# -------------------------------------------------
# 8) Festival (composição com Palco)              🡇
# -------------------------------------------------
class Festival():
    def __init__(self, nome:str, data:date, local:str, palco: Palco):
        self.nome = nome
        self.data = data
        self.local = local
        self.clientes = []
        self.equipe = []
        self.ingressos = []
        self.palco = palco

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
    __auditores = []
    
    def __init__(self, nome):
        super().__init__()
        self.nome = nome
        self.__auditores.append(self)
        self.festivais_analisados = dict()

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
            
        self.festivais_analisados[fest.nome] = conformidade
        
    @classmethod
    def gerar_relatorio_geral(cls):
        conteudo = str()
        for objeto in cls.__auditores:
            msg = f"Auditor : {objeto.nome} , analises : "
            for key,value in objeto.festivais_analisados.items():
                palco = key
                if value:
                    msg += f' "{palco}" em conformidade'
                else:
                    msg += f' {palco} não estava em conformidade'
            conteudo += f'{msg} \n'
            
        editor_arquivo = Relatorio(ARQUIVO_RELATORIO)
        editor_arquivo.rescrever_arquivo(conteudo)
                    
        
        
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

    empresa = EmpresaEventos("Top Eventos")

    # --- palcos ---
    palco_grande = Palco("Principal", capacidade=3)   # capacidade pequena para testar excesso
    palco_pequeno = Palco("Alternativo", capacidade=100)

    # --- festivais ---
    fest1 = Festival("MiniFest", date(2025, 9, 1), "Parque A", palco_grande)
    # Observação: a classe Festival não define self.palco no __init__ no seu código original,
    # então garantimos o atributo aqui:
    fest1.palco = palco_grande

    fest2 = Festival("MegaFest", date(2025, 10, 5), "Estádio B", palco_pequeno)
    fest2.palco = palco_pequeno

    empresa.adicionar_festival(fest1)
    empresa.adicionar_festival(fest2)

    # --- clientes ---
    c1 = Cliente("Ana", "11111111111", "ana@email.com")
    c2 = Cliente("Bruno", "22222222222", "bruno@email.com")
    c3 = Cliente("Carla", "33333333333", "carla@email.com")
    c4 = Cliente("Daniel", "44444444444", "daniel@email.com")

    # --- ingressos ---
    i1 = Ingresso("I001", "Pista", 120.0)
    i2 = Ingresso("I002", "VIP", 300.0)
    i3 = Ingresso("I003", "Pista", 120.0)
    i4 = Ingresso("I004", "Pista", 120.0)

    # --- vender ingressos para fest1 (palco_grande cap=3) ---
    print("\n--- Vendas MiniFest ---")
    fest1.vender_ingresso(c1, i1)   # venda ok
    fest1.vender_ingresso(c2, i2)   # venda ok
    fest1.vender_ingresso(c3, i3)   # venda ok (alcança capacidade)
    # testar capacidade excedida
    fest1.vender_ingresso(c4, i4)   # deve imprimir "Ingressos esgotados!"

    # tentar vender ingresso duplicado para c1
    fest1.vender_ingresso(c1, i2)   # deve dizer que cliente já possui ingresso

    # --- vender ingressos para fest2 ---
    print("\n--- Vendas MegaFest ---")
    fest2.vender_ingresso(c4, i4)   # venda ok

    # --- adicionar funcionários ---
    f1 = Funcionario("Felipe", "55555555555", "Segurança", "REG001")
    f2 = Funcionario("Mariana", "66666666666", "Produção", "REG002")

    fest1.adicionar_funcionario(f1)
    fest2.adicionar_funcionario(f2)

    # --- listar participantes e ingressos ---
    print("\n--- Dados MiniFest ---")
    fest1.listar_clientes()
    fest1.listar_equipe()
    fest1.listar_ingressos()

    print("\n--- Dados MegaFest ---")
    fest2.listar_clientes()
    fest2.listar_equipe()
    fest2.listar_ingressos()

    # --- auditor ---
    auditor = Auditor("Lucas")
    # opcional: não chamamos auditor.logar_entrada() porque a classe Auditor, como está,
    # chama log_evento (que pertence a AuditavelMixin) e AuditavelMixin não é herdado por Auditor
    # no seu código atual — para evitar AttributeError, pulamos logar_entrada aqui.

    print("\n--- Auditoria MiniFest ---")
    auditor.auditar_festival(fest1)

    print("\n--- Auditoria MegaFest ---")
    auditor.auditar_festival(fest2)

    # --- listar festivais na empresa ---
    print("\n--- Festivais da Empresa ---")
    empresa.listar_festivais()
    
    Cliente.gerar_relatorio_ingresos_geral()
    Auditor.gerar_relatorio_geral()

    """
    TODO:
      • Crie 1 empresa, 2 festivais, clientes, equipe e auditor.
      • Venda ingressos, liste participantes, audite festivais.
      • Mostre saídas no console para validar implementações.
    """
    pass

