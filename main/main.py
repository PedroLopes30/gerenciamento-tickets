# Imports
from sistema_festival import Cliente, Funcionario, Ingresso, Festival, EmpresaEventos, Auditor
from datetime import date

# -------------------------------------------------
# 11) Bloco de teste                              🡇
# -------------------------------------------------
if __name__ == "__main__":
    """
    TODO:
      • Crie 1 empresa, 2 festivais, clientes, equipe e auditor.
      • Venda ingressos, liste participantes, audite festivais.
      • Mostre saídas no console para validar implementações.
    """

    print("\n" + "="*50)
    print("TESTANDO A IMPLEMENTAÇÃO".center(50))
    print("="*50 + "\n")

    # Criando empresa
    try:
        empresa = EmpresaEventos("Rock in Rio Produções")
        print(f"Empresa criada: {empresa.nome}")
    except ValueError as error:
        print(f"Erro ao criar empresa: {error}")

    # Criando festivais
    festival1 = Festival("Rock in Rio", date(2024, 9, 15), "Parque Olímpico", "Palco Mundo", 100000)
    festival2 = Festival("Lollapalooza", date(2024, 3, 22), "Autódromo de Interlagos", "Palco Onix", 50000)

    empresa.adicionar_festival(festival1)
    empresa.adicionar_festival(festival2)
    print("\nFestivais adicionados:")
    empresa.listar_festivais()

    # Criando clientes
    cliente1 = Cliente("João Silva", "123.456.789-00", "joao@email.com")
    cliente2 = Cliente("Maria Souza", "987.654.321-00", "maria@email.com")
    cliente3 = Cliente("Carlos Oliveira", "456.789.123-00", "carlos@email.com")

    # Criando ingressos
    ingresso1 = Ingresso("P001", "Pista", 350.00)
    ingresso2 = Ingresso("V001", "VIP", 800.00)
    ingresso3 = Ingresso("B001", "Backstage", 1200.00)

    # Vendendo ingressos
    print("\nVendendo ingressos:")
    festival1.vender_ingresso(cliente1, ingresso1)
    festival1.vender_ingresso(cliente2, ingresso2)
    festival2.vender_ingresso(cliente3, ingresso3)

    # Tentando vender ingresso duplicado
    print("\nTentando vender ingresso duplicado:")
    festival1.vender_ingresso(cliente1, ingresso1)

    # Criando funcionários
    func1 = Funcionario("Ana Santos", "111.222.333-44", "Produtora", "FUNC001")
    func2 = Funcionario("Pedro Rocha", "555.666.777-88", "Segurança", "FUNC002")

    # Adicionando funcionários aos festivais
    festival1.adicionar_funcionario(func1)
    festival2.adicionar_funcionario(func2)

    # Logando entrada de funcionários
    print("\nLogando entrada de funcionários:")
    func1.logar_entrada()
    func2.logar_entrada()

    # Exibindo dados dos funcionários
    print("\nDados dos funcionários:")
    func1.exibir_dados()
    func2.exibir_dados()

    # Listando participantes
    print("\nListando clientes do Rock in Rio:")
    festival1.listar_clientes()
    print("\nListando equipe do Rock in Rio:")
    festival1.listar_equipe()

    print("\nListando clientes do Lollapalooza:")
    festival2.listar_clientes()
    print("\nListando equipe do Lollapalooza:")
    festival2.listar_equipe()

    # Criando e testando auditor
    auditor = Auditor("Roberto Almeida")
    print(f"\nAuditor criado: {auditor}")

    # Logando entrada do auditor
    auditor.logar_entrada()

    # Auditando festivais
    print("\nAuditando festivais:")
    print("\nAuditoria Rock in Rio:")
    auditor.auditar_festival(festival1)

    print("\nAuditoria Lollapalooza:")
    auditor.auditar_festival(festival2)

    # Testando listagem de ingressos
    print("\nIngressos do Rock in Rio:")
    festival1.listar_ingressos()

    print("\nIngressos do Lollapalooza:")
    festival2.listar_ingressos()

    # Testando métodos dos clientes
    print("\nIngressos do João Silva:")
    cliente1.listar_ingressos()

    print("\n" + "="*50)
    print("FIM DOS TESTES".center(50))
    print("="*50 + "\n")

