import textwrap
from abc import abstractmethod,ABC
from datetime import datetime

class Cliente:

    def __init__(self,endereco,):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento     

class Conta:

    def __init__(self,cliente,numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero_conta):
        return cls(cliente,numero_conta)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self,saque):
        saldo = self._saldo

        if saque>saldo:
            print("Erro ao sacar. Valor excedeu o saldo da sua conta!")
        elif saque>0:
            self._saldo += saque 
            print("Saque efetua com sucesso!")
            return True
        else:
            print("Erro ao sacar. Valor inválido...")

        return False

    def depositar(self,deposito):
        if deposito>0:
            self._saldo += deposito
            print("Depóstio efetuado com sucesso.")
            return True
        else:
            print("Erro ao depositar. Valor inválido...")
            return False

class ContaCorrente(Conta):

    def __init__(self, numero, cliente,limite=500,limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self,valor):
        numeros_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'=='Saque']])

        if valor>self._limite:
            print("Erro ao sacar. Valor excedeu o limite")
        elif numeros_saques>self._limite_saque:
            print("Erro ao sacar. Foi excedido o limte de saques diário...")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"

class Historico:

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                'tipo':transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now()

            }
        )

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):

    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        transacao_efetuada = conta.depositar(self.valor)

        if transacao_efetuada:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):

    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        transacao_efetuada = conta.sacar(self.valor)

        if transacao_efetuada:
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Cliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = input("D - Depositar\nS - Sacar\nE - Extrato\nCA - Cadastrar\nCC - Criar Conta\nLC - Listar Contas\nQ - Sair\nInforme uma das ações acima: ").upper()

        if opcao == "D":
            depositar(clientes)

        elif opcao == "S":
            sacar(clientes)

        elif opcao == "E":
            exibir_extrato(clientes)

        elif opcao == "CA":
            criar_cliente(clientes)

        elif opcao == "CC":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "LC":
            listar_contas(contas)

        elif opcao == "Q":
            print("Saindo...")
            break

        else:
            print("Informe um opção válida.")


main()
