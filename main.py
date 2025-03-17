import textwrap
# -*- coding: utf-8 -*-

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    @staticmethod
    def filtrar_usuario(cpf, usuarios):
        for usuario in usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None


class Conta:
    AGENCIA = "0001"

    def __init__(self, numero_conta, usuario):
        self.agencia = Conta.AGENCIA
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""
        self.numero_saques = 0
        self.limite = 500
        self.limite_saques = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Deposito:	R$ {valor:.2f}\n"
            print("\n=== Deposito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:		R$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:		R$ {self.saldo:.2f}")
        print("==========================================")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        if Usuario.filtrar_usuario(cpf, self.usuarios):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = Usuario.filtrar_usuario(cpf, self.usuarios)

        if usuario:
            numero_conta = len(self.contas) + 1
            conta = Conta(numero_conta, usuario)
            self.contas.append(conta)
            usuario.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""
                Agência:	{conta.agencia}
                C/C:		{conta.numero_conta}
                Titular:	{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def menu(self):
        while True:
            opcao = input(textwrap.dedent("""
                ================ MENU ================
                [d]\tDepositar
                [s]\tSacar
                [e]\tExtrato
                [nc]\tNova conta
                [lc]\tListar contas
                [nu]\tNovo usuário
                [q]\tSair
                => """))

            if opcao == "d":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = Usuario.filtrar_usuario(cpf, self.usuarios)
                if usuario and usuario.contas:
                    valor = float(input("Informe o valor do depósito: "))
                    usuario.contas[0].depositar(valor)
                else:
                    print("@@@ Usuário ou conta não encontrados. @@@")

            elif opcao == "s":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = Usuario.filtrar_usuario(cpf, self.usuarios)
                if usuario and usuario.contas:
                    valor = float(input("Informe o valor do saque: "))
                    usuario.contas[0].sacar(valor)
                else:
                    print("@@@ Usuário ou conta não encontrados. @@@")

            elif opcao == "e":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = Usuario.filtrar_usuario(cpf, self.usuarios)
                if usuario and usuario.contas:
                    usuario.contas[0].exibir_extrato()
                else:
                    print("@@@ Usuário ou conta não encontrados. @@@")

            elif opcao == "nu":
                self.criar_usuario()
            elif opcao == "nc":
                self.criar_conta()
            elif opcao == "lc":
                self.listar_contas()
            elif opcao == "q":
                break
            else:
                print("Operação inválida, tente novamente.")


if __name__ == "__main__":
    banco = Banco()
    banco.menu()
