from constants import DEFAULT_COMMA_CODE

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
          splitted_values = normalized_string.split('||')
          
          for without_pipes_string in splitted_values:
            # unpacking em dois valores do array 'chave:valor'
            key, value = without_pipes_string.split(':')

            transaction[key] = value

          transactions.append(transaction)

        self.transactions = transactions

  def add_transaction_in_db(self, transaction):
    last_transaction = self.transactions[-1]
    last_id = int(last_transaction['id'])

    transaction['id']= last_id + 1

    parsed_keys_and_values = []
    transaction_items = transaction.items()

    for index, key_and_value_tuple in enumerate(transaction_items):
      key, value = key_and_value_tuple
      is_last_item = index == len(transaction_items) - 1
      parsed_keys_and_values.append(f'{key}:{value}'if is_last_item  else f'{key}:{value}||')
    
    transaction_string = ',' + ''.join(parsed_keys_and_values)

    db = open('transactions.csv', 'a')
    db.write(transaction_string)
    db.close()
    self.get_all_from_db()

  def __init__(self):
    self.get_all_from_db()
