saldo = 0
limite = 500
extrato = ""
numeros_saques = 3
historico_saques = ""
historico_depositos = ""

while True:
    opcao = input("D - Depositar\nS - Sacar\nE - Extrato\nQ - Sair\nInforme uma das ações acima: ").upper()
    if(opcao == 'D'):
        deposito = float(input("Informe o valor do depósito: "))
        if(deposito>0):
            saldo+=deposito 
            historico_depositos += f"{deposito:.2f} "
            print("Depósito efetuado com sucesso!")
        else:
            print("Erro ao realizar depósito. Verifique o valor informado.")
    elif(opcao == 'S'):
        if(numeros_saques!=0):
            saque = float(input("Informe o valor do saque: "))
            if(saque>0):
                if(saque>saldo):
                    print("Não possui saldo suficinte.")
                else:
                    if(saque>limite):
                        print("Valor solicitado acima do limite definido por saque.")
                    else:
                        saldo-=saque
                        historico_saques += f"{saque:.2f} "
                        numeros_saques-=1   
                        print("Saque efetuado com sucesso!")
            else:
                print("Erro ao realizar saque. Verifique o valor informado.")
        else:
            print("Limite diário de saques atingidos.")
    elif(opcao=='E'):
        if(historico_saques!="" or historico_depositos!=""):
            extrato = f"Dépositos feitos: {historico_depositos}\nSaques Feitos: {historico_saques}\nSaldo: R$ {saldo:.2f}"
        if(extrato==""):
            print("Não foram realizados movimentações")
        else:
            print(extrato)
    elif(opcao=='Q'):
        print("Saindo...")
        break
    else:
        print("Informe um opção válida.")