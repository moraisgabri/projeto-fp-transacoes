from Controllers.Constants import DEFAULT_COMMA_CODE
class TransactionController: 
  transactions = []

  def get_all_from_db(self):
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

  def add_transaction_in_db(self, transaction):
    last_transaction = self.transactions[-1]
    last_id = int(last_transaction['id'])

    transaction['id'] = last_id + 1

    parsed_keys_and_values = []
    transaction_items = transaction.items()

    for index, key_and_value_tuple in enumerate(transaction_items):
      key, value = key_and_value_tuple
      is_last_item = index == len(transaction_items) - 1
      parsed_keys_and_values.append(f'{key}:{value}'if is_last_item  else f'{key}:{value};')
    
    transaction_string = ',' + ''.join(parsed_keys_and_values)

    db = open('transactions.csv', 'a')
    db.write(transaction_string)
    db.close()
    self.get_all_from_db()

  def get_transaction_by_id(self, id):
    for transaction in self.transactions:
      if transaction['id'] == id:
        return transaction
    
  def delete_transaction_by_id(self, id):
    transaction = self.get_transaction_by_id(id)
    transaction_index = self.transactions.index(transaction)
    del self.transactions[transaction_index]

    self.update_db()

  def update_transaction_by_id(self, id, new_transaction):
    transaction = self.get_transaction_by_id(id)
    transaction_index = self.transactions.index(transaction)

    self.transactions[transaction_index] = new_transaction

    self.update_db()

  def update_db(self):
    db = open('transactions.csv', 'w')
    db.write('')
    db.close()

    csv = ''

    for transaction in self.transactions:
      parsed = self.parse_to_csv(transaction)
      csv += parsed + ',' if transaction != self.transactions[-1] else parsed
    
    db = open('transactions.csv', 'a')
    db.write(csv)

  def parse_to_csv(self, transaction):
    parsed_keys_and_values = []
    transaction_items = transaction.items()

    for index, key_and_value_tuple in enumerate(transaction_items):
      key, value = key_and_value_tuple
      is_last_item = index == len(transaction_items) - 1
      parsed_keys_and_values.append(f'{key}:{value}'if is_last_item  else f'{key}:{value};')
    
    return ''.join(parsed_keys_and_values)
  
  def get_transactions_by_category(self, category):
    transactions = []
    for transaction in self.transactions:
      if transaction['category'] == category:
        transactions.append(transaction)
    
    return transactions

  def __init__(self):
    self.get_all_from_db()
