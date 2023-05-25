from Controllers.Constants import DEFAULT_COMMA_CODE
import smtplib
class TransactionController:
  transactions = []

  def get_all_from_db(self):
    try:
      with open('transactions.csv') as data:
        db_data = data.read()

        db_data_array = db_data.split(',')
        transactions = []

        for db_transaction in db_data_array:
          transaction = {}
          # Normalizando as víruglas para evitar que conflitem com csv
          normalized_string = db_transaction.replace(DEFAULT_COMMA_CODE, ',')

          # Removendo as divisões entre chaves e valores
          splitted_values = normalized_string.split(';')

          for without_pipes_string in splitted_values:
            # unpacking em dois valores do array 'chave:valor'
            key, value = without_pipes_string.split(':')

            transaction[key] = value

          transactions.append(transaction)

        self.transactions = transactions
        return transactions
    except:
      print('Erro ao buscar as transações no banco de dados.')

  def add_transaction_in_db(self, transaction):
    try: 
      last_transaction = self.transactions[-1] if len(self.transactions) > 0 else {'id': 0}
      last_id = int(last_transaction['id'])

      transaction['id'] = last_id + 1

      parsed_keys_and_values = []
      transaction_items = transaction.items()

      for index, key_and_value_tuple in enumerate(transaction_items):
        key, value = key_and_value_tuple
        is_last_item = index == len(transaction_items) - 1
        parsed_keys_and_values.append(f'{key}:{value}'if is_last_item  else f'{key}:{value};')

      transaction_string = ',' + ''.join(parsed_keys_and_values) if last_id > 0 else ''.join(parsed_keys_and_values)

      db = open('transactions.csv', 'a')
      db.write(transaction_string)
      db.close()
      self.get_all_from_db()
    except:
      print('Erro ao adicionar a transação.')

  def get_transaction_by_id(self, id):
    try:
      for transaction in self.transactions:
        if transaction['id'] == id:
          return transaction
    except:
      print('Erro ao buscar a transação.')

  def delete_transaction_by_id(self, id):
    try:
      transaction = self.get_transaction_by_id(id)
      transaction_index = self.transactions.index(transaction)
      del self.transactions[transaction_index]

      self.update_db()
    except:
      print('Erro ao deletar a transação.')

  def update_transaction_by_id(self, id, new_transaction):
    try:
      transaction = self.get_transaction_by_id(id)
      transaction_index = self.transactions.index(transaction)

      self.transactions[transaction_index] = new_transaction

      self.update_db()
    except:
      print('Erro ao atualizar a transação.')

  def update_db(self):
    try:
      db = open('transactions.csv', 'w')
      db.write('')
      db.close()

      csv = ''

      for transaction in self.transactions:
        parsed = self.parse_to_csv(transaction)
        csv += parsed + ',' if transaction != self.transactions[-1] else parsed

      db = open('transactions.csv', 'a')
      db.write(csv)
    except:
      print('Erro ao atualizar o banco de dados.')


  def parse_to_csv(self, transaction):
    try:
      parsed_keys_and_values = []
      transaction_items = transaction.items()

      for index, key_and_value_tuple in enumerate(transaction_items):
        key, value = key_and_value_tuple
        is_last_item = index == len(transaction_items) - 1
        parsed_keys_and_values.append(f'{key}:{value}'if is_last_item  else f'{key}:{value};')

      return ''.join(parsed_keys_and_values)
    except:
      print('Erro ao converter para csv.')

  def get_transactions_by_category(self, category):
    try:
      transactions = []
      for transaction in self.transactions:
        if transaction['category'] == category:
          transactions.append(transaction)

      return transactions
    except:
      print('Erro ao buscar transações por categoria.')

  def send_data_by_email(self, email):
    try:
      transactions = self.get_all_from_db()
      transactions_string = '\nSeu resumo de transações: \n\nTotal de transações: ' + str(len(transactions)) + '\n\n'

      for transaction in transactions:
        transactions_string += f'Id da transação: {transaction["id"]}, Nome: {transaction["name"]}, Categoria: {transaction["category"]}, Valor: {transaction["value"]} \n'

      server = smtplib.SMTP('smtp-mail.outlook.com: 587')
      server.starttls()
      server.login("projetoipcesar@outlook.com", "projetoip10")
      server.sendmail("projetoipcesar@outlook.com", email, transactions_string.encode('utf-8'))
      server.quit()
    except:
      print('Erro ao enviar email.')

  def __init__(self):
    self.get_all_from_db()
