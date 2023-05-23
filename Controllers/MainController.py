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
    print("6 - Sair \n")
    option = input(">> ")
    if option == '1':
      MainController.list_all_transactions()
    
    return option
  
  def format_matrix(header, matrix,
                  top_format, left_format, cell_format, row_delim, col_delim):
    table = [[''] + header] + [[name] + row for name, row in zip(header, matrix)]
    table_format = [['{:^{}}'] + len(header) * [top_format]] \
                 + len(matrix) * [[left_format] + len(header) * [cell_format]]
    col_widths = [max(
                      len(format.format(cell, 0))
                      for format, cell in zip(col_format, col))
                  for col_format, col in zip(zip(*table_format), zip(*table))]
    return row_delim.join(
               col_delim.join(
                   format.format(cell, width)
                   for format, cell, width in zip(row_format, row, col_widths))
               for row_format, row in zip(table_format, table))
  
  def list_all_transactions():
    transactions = TransactionController.get_all_from_db(TransactionController())
    os.system('cls')

    print("Lista de transações: \n")

    transactionsValues = []
    for i in range(len(transactions)):
      transactionsValues.append([transactions[i]['id'], transactions[i]['category'], transactions[i]['name'], transactions[i]['value']])

    print(MainController.format_matrix(['ID', 'Categoria', 'Nome', 'Valor'], transactionsValues, '{:^{}}', '{:<{}}', '{:<{}}', '\n', '\t\t'))

    input("\nPressione ENTER para voltar ao menu principal...")
    os.system('cls')
    MainController.main_menu()
    
      
