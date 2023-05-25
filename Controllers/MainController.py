from Controllers.DataController import TransactionController
import os
import smtplib

transactionController = TransactionController()


class MainController:
    def main_menu():
        print("Bem vindo, ao seu gerenciador de transações financeiras!")
        print("\nEscolha uma opção: \n")
        print("1 - Listar todas as transações")
        print("2 - Adicionar uma nova transação")
        print("3 - Buscar uma transação por id")
        print("4 - Deletar uma transação por id")
        print("5 - Listar transações por categoria")
        print("6 - Editar uma transação por id")
        print("7 - Enviar dados por e-mail")
        print("8 - Sair \n")
        option = input(">> ")

        if option == '1':
            MainController.list_all_transactions()
        elif option == '2':
            MainController.add_new_transaction()
        elif option == '3':
            MainController.search_transaction_by_id()
        elif option == '4':
            MainController.delete_transaction_by_id()
        elif option == '5':
            MainController.list_transactions_by_category()
        elif option == '6':
            MainController.update_transaction_by_id()
        elif option == '7':
            MainController.send_data_by_email()
        elif option == '8':
            exit()

        return option
    
    def isNumber(n):
      try:
        float(n)
      except ValueError:
            return False
      return True

    def return_main_menu():
          try: 
            input("\nPressione ENTER para voltar ao menu principal...")
            os.system('cls')
            MainController.main_menu()
          except:
              return

    def list_all_transactions():
        try:
          transactions = TransactionController.get_all_from_db(
              transactionController)
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

          return MainController.return_main_menu()

        except:
            print('Erro ao listar todas as transações.')
            return MainController.return_main_menu()



    def add_new_transaction():
        try:
          os.system('cls')
          print("Adicionar uma nova transação: \n")
          category = input("Categoria: ")
          name = input("Nome: ")
          value = input("Valor: ")

          if not MainController.isNumber(value):
            print('O valor deve ser um número.')
            return MainController.return_main_menu()


          transaction = {
              'category': category.replace(',', ' ').replace(';', ' '),
              'name': name.replace(',', ' ').replace(';', ' '),
              'value': value.replace(',', ' ').replace(';', ' ')
          }

          if transaction['category'].replace(" ", "") == '' or transaction['name'].replace(" ", "") == '' or transaction['value'].replace(" ", "") == '':
              print("\nTodos os campos são obrigatórios!")
              return MainController.return_main_menu()

          TransactionController.add_transaction_in_db(
              transactionController, transaction)

          print("\nTransação adicionada com sucesso!")
          return MainController.return_main_menu()

        except:
            print('Erro ao adicionar nova transação.')
            return MainController.return_main_menu()

            

    def search_transaction_by_id():
        try: 
          os.system('cls')
          print("Buscar transação por id: \n")
          id = input("Id: ")

          transaction = TransactionController.get_transaction_by_id(
              transactionController, id)

          if transaction == None:
              print("\nTransação não encontrada!")
              return MainController.return_main_menu()

          else:
              print("\nTransação encontrada:")
              print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  "ID", "Categoria", "Nome", "Valor"))
              print("-" * 65)
              print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  transaction['id'], transaction['category'], transaction['name'], transaction['value']))

              return MainController.return_main_menu()

        except:
            print('Erro ao buscar transação por id.')
            return MainController.return_main_menu()

    
    def delete_transaction_by_id():
        try:
          os.system('cls')
          print("Deletar transação por id: \n")
          id = input("Id: ")

          transaction = TransactionController.get_transaction_by_id(
              transactionController, id)

          if transaction == None:
              print("\nTransação não encontrada!")
              return MainController.return_main_menu()

          else:
              TransactionController.delete_transaction_by_id(transactionController, id)
              print("\nTransação deletada com sucesso!")
              return MainController.return_main_menu()

        except:
            print('Erro ao deletar transação por id.')
            return MainController.return_main_menu()


    
    def list_transactions_by_category():
        try:
          os.system('cls')
          print("Listar transações por categoria: \n")
          category = input("Categoria: ")

          transactions = TransactionController.get_transactions_by_category(transactionController, category)

          if transactions == []:
              print("\nNão há transações nessa categoria!")
              return MainController.return_main_menu()

          else:
              print("\nTransações encontradas:")
              print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  "ID", "Categoria", "Nome", "Valor"))
              print("-" * 65)
              for transaction in transactions:
                  print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  transaction['id'], transaction['category'], transaction['name'], transaction['value']))

              return MainController.return_main_menu()

        except:
            print('Erro ao listar transações por categoria.')
            return MainController.return_main_menu()



    def update_transaction_by_id():
        try:
          os.system('cls')
          print("Editar transação por id: \n")
          id = input("Id: ")

          transaction = TransactionController.get_transaction_by_id(
              transactionController, id)

          if transaction == None:
              print("\nTransação não encontrada!")
              return MainController.return_main_menu()

          else:
              print("\nTransação encontrada:")
              print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  "ID", "Categoria", "Nome", "Valor"))
              print("-" * 65)
              print("{: ^5} {: ^20} {: ^20} {: ^20}".format(
                  transaction['id'], transaction['category'], transaction['name'], transaction['value']))

              print("\nDigite os novos dados da transação: \n")
              category = input("Categoria: ")
              name = input("Nome: ")
              value = input("Valor: ")

              if not MainController.isNumber(value):
                print('O valor deve ser um número.')
                return MainController.return_main_menu()


              newTransaction = {
                  'category': category.replace(',', ' ').replace(';', ' '),
                  'name': name.replace(',', ' ').replace(';', ' '),
                  'value': value.replace(',', ' ').replace(';', ' '),
                  'id': id
              }

              if newTransaction['category'].replace(" ", "") == '' == '' or newTransaction['name'].replace(" ", "") ==  '' or newTransaction['value'].replace(" ", "") == '':
                  print("\nTodos os campos são obrigatórios!")
                  return MainController.return_main_menu()

              TransactionController.update_transaction_by_id(transactionController, id, newTransaction)

              print("\nTransação atualizada com sucesso!")
              return MainController.return_main_menu()

        except:
            print('Erro ao atualizar transação por id.')
            return MainController.return_main_menu()



    def send_data_by_email():
      try:
        os.system('cls')
        print("Enviar dados por e-mail: \n")
        email = input("E-mail: ")

        TransactionController.send_data_by_email(transactionController, email)

        print("\nDados enviados com sucesso!")
        return MainController.return_main_menu()

      except:
          print('Erro ao enviar dados por e-mail.')
          return MainController.return_main_menu()

