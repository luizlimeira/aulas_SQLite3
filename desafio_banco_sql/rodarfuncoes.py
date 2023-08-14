from database import *

while True:
    print('-'*20)
    print("Selecione uma opção: ")
    print("1-Criar conta")
    print("2-Verificar saldo")
    print("3-Depositar dinheiro")
    print("4-Sacar dinheiro")
    print("5-Encerrar")
        
    opcoes = str(input("Opção: "))
    print()

    if opcoes == "1":
        create_user()

    elif opcoes == "2":
        balance()

    elif opcoes == "3":
        deposit()

    elif opcoes == "4":
        whithdraw()

    elif opcoes == "5":
        break_program()
        break

    else:
        print("Opção Inválida, tente novamente")