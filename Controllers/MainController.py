from Controllers.DataController import TransactionController
import os


class MainController:
    def main_menu():
        print("Bem vindo, ao seu gerenciador de transações financeiras!")
        print("\nEscolha uma opção: \n")
        print("1 - Listar todas as transações")
        print("2 - Adicionar uma nova transação")
        print("3 - Buscar uma transação por id")
        print("4 - Deletar uma transação por id")
        print("5 - Listar transações por categoria")
        print("6 - Enviar dados por e-mail")
        print("7 - Sair \n")
        option = input(">> ")
        if option == '1':
            MainController.list_all_transactions()
        elif option == '2':
            MainController.add_new_transaction()
        elif option == '6':
            exit()

        return option

    def list_all_transactions():
        transactions = TransactionController.get_all_from_db(
            TransactionController())
        os.system('cls')

        print("Lista de transações: \n")

        transactionsValues = []
        for i in range(len(transactions)):
            transactionsValues.append([transactions[i]['id'], transactions[i]
                                      ['category'], transactions[i]['name'], transactions[i]['value']])

        print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
            "ID", "Categoria", "Nome", "Valor"))
        print("-" * 65)
        for row in transactionsValues:
            print("{: ^5} {: ^20} {: ^20} {: ^20}".format(*row))

        input("\nPressione ENTER para voltar ao menu principal...")
        os.system('cls')
        MainController.main_menu()

    def add_new_transaction():
        os.system('cls')
        print("Adicionar uma nova transação: \n")
        category = input("Categoria: ")
        name = input("Nome: ")
        value = input("Valor: ")

        transaction = {
            'category': category,
            'name': name,
            'value': value
        }

        TransactionController.add_transaction_in_db(
            TransactionController(), transaction)

        print("\nTransação adicionada com sucesso!")
        input("\nPressione ENTER para voltar ao menu principal...")
        os.system('cls')
        MainController.main_menu()
