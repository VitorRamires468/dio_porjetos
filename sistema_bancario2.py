saldo = 0
limite = 500
extrato = ""
numeros_saques = 3
historico_saques = ""
historico_depositos = ""
usuarios = []
contas = []
numero_conta = 0

def verifcarCpf(cpf):
    cpf_exite = False
    if(len(usuarios)!=0):
        for users in usuarios:
            if cpf == users['cpf']:
                cpf_exite = True
    
    return cpf_exite 

def cadastrar():
    cpf = input("Informe seu CPF: ")
    cpf_exite = verifcarCpf(cpf)
    if cpf_exite:
        print("Erro ao criar usuário. CPF vinculado a uma usuário.")
        return 
    nome_cadastro = input("Informe seu nome: ")
    data_nascimento = input("Informe sua data de nascimento (DD/MM/AAAA): ")
    endereco = input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    user = {'nome':nome_cadastro,'data':data_nascimento,'cpf':cpf,'endereco':endereco}
    usuarios.append(user)
        
def criarConta():
    global numero_conta
    cpf  = input("Informe seu cpf: ")
    cpf_existe = verifcarCpf(cpf)
    if cpf_existe:
        nome_conta = input("Informe seu nome: ")
        numero_conta+=1
        conta_criada = {
            'nome':nome_conta,
            'conta':f"0001-{str(numero_conta)}",
        }
        contas.append(conta_criada)
        print("Conta Corrente criada com sucesso")
        return
    print("Erro ao criar conta corrente. CPF não consta no nosso banco de dados...")
    

def sacar(*,saque,saldo,extrato_saque,numero_saque):
    if(numeros_saques!=0):
        if(saque>0):
            if(saque>saldo):
                print("Não possui saldo suficinte.")
            else:
                if(saque>limite):
                    print("Valor solicitado acima do limite definido por saque.")
                else:
                    saldo-=saque
                    extrato_saque += f"{saque:.2f} "
                    numero_saque-=1   
                    print("Saque efetuado com sucesso!")
                    return saldo,extrato_saque,numero_saque
        else:
            print("Erro ao realizar saque. Verifique o valor informado.")
    else:
        print("Limite diário de saques atingidos.")

def depositar(deposito,saldo,extrato_deposito,/):
    if(deposito>0):
        saldo+=deposito 
        extrato_deposito += f"{deposito:.2f} "
        print("Depósito efetuado com sucesso!")
        return saldo,extrato_deposito
    else:
        print("Erro ao realizar depósito. Verifique o valor informado.")

def mostrar_extrato(saldo,/,*,extrato):
    if(extrato==""):
        print("Não foram realizados movimentações")
    else:
        extrato+=f"\nSaldo: R$ {saldo:.2f}"
        print(extrato)

def listarContas(contas):
    print("-----------------------------------------------")
    if(len(contas)==0):
        print('Nenhuma foi criada ainda')
    else:
        for conta in contas:
            print(f"{conta['nome']} - {conta['conta']}")
    print("-----------------------------------------------")

def main():
    while True:
        opcao = input("D - Depositar\nS - Sacar\nE - Extrato\nCA - Cadastrar\nCC - Criar Conta\nLC - Listar Contas\nQ - Sair\nInforme uma das ações acima: ").upper()
        if(opcao == 'D'):
            deposito = float(input("Informe o valor do depósito: "))
            retorno_deposito = depositar(deposito,saldo,historico_depositos)
            if(retorno_deposito!=None):
                saldo,historico_depositos = retorno_deposito
        elif(opcao == 'S'):
            saque = float(input("Informe o valor do saque: "))
            retorno_saque = sacar(saque=saque,saldo=saldo,extrato_saque=historico_saques,numero_saque=numeros_saques)
            if(retorno_saque!=None):
                saldo, historico_saques,numeros_saques = retorno_saque
        elif(opcao=='E'):
            if(historico_saques!="" or historico_depositos!=""):
                extrato = f"Dépositos feitos: {historico_depositos}\nSaques Feitos: {historico_saques}"
            mostrar_extrato(saldo,extrato=extrato)
        elif(opcao=='CA'):
            cadastrar()
        elif(opcao=='CC'):
            criarConta()
        elif(opcao=='LC'):
            listarContas(contas)
        elif(opcao=='Q'):
            print("Saindo...")
            break
        else:
            print("Informe um opção válida.")

main()