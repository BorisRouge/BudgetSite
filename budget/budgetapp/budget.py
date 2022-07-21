from unicodedata import decimal
from decimal import Decimal as dec


class Category (object):
  def __init__(self, category_name, balance = 0,ledger = []):
    deposit_counter = 0                                      
    withdrawal_counter = 0                                   
    self.Category = Category #is it needed?
    self.category_name = category_name
    self.ledger = ledger
    self.balance = balance
    self.deposit_counter = deposit_counter                   
    self.withdrawal_counter = withdrawal_counter             

  def display (self): #to be deleted, was moved to an external function to be mapped with the database
    title_line = f'{self.category_name}'.center (30, "*")
    lines = []
    i = 0
    total = 0
    while i < len(self.ledger):                                #  
      item = self.ledger[i]                                    #formatting
      n = len(item['description'])                             #     
      if n > 23:
        n = 23      
      lines.append(str(item['description'])[:23]+"{:.2f}".format(float(item['amount'])).rjust(30-n))
      total += float(item['amount'])
      i+= 1

    result = f'{title_line}\n'
                                                              #
    for x in lines:                                           # result 
      result += f'{x}\n'                                      #
    result += f'Total: {"{:.2f}".format(total)}'
    
    return result

  
  def deposit (self, amount, description = ''):
    item = {"amount": amount, "description": description}
    self.ledger.append (item)
    self.balance +=dec(amount)
    self.deposit_counter +=dec(amount)

  def withdraw (self, amount, description = ''):
    amount = dec(amount)
    if self.balance >= dec(amount):
      item = {"amount": -amount, "description": description}
      self.ledger.append (item)
      self.balance -=dec(amount)
      self.withdrawal_counter +=dec(amount)
      return True
    else:
      print("Faulty withdraw")
      return False
  
  def get_balance (self):
    return self.balance

  def check_funds (self, amount):
    if amount > self.balance:
      return False
    else: 
      return True



  def transfer (self, amount, category_name):        
    b = self.balance
    self.withdraw (amount, f'Transfer to {category_name.category_name}') 
    if b > self.balance:
      category_name.deposit (amount, f'Transfer from {self.category_name}')
      return True
    else:
      return False

  ### PRINT OUTPUT ###
  def print(self):
    title_line = f'{self.category_name}'.center (30, "*")
    lines = []
    i = 0
    total = 0
    while i < len(self.ledger):                                #  
      item = self.ledger[i]                                    #formatting
      n = len(item['description'])                             #     
      if n > 23:
        n = 23      
      lines.append(str(item['description'])[:23]+"{:.2f}".format(float(item['amount'])).rjust(30-n))
      total += float(item['amount'])
      i+= 1             
              
    result = f'{title_line}\n'
                                                              #
    for x in lines:                                           # result 
      result += f'{x}\n'                                      #
    result += 'Total:',"{:.2f}".format(total)
    
    return result
    
    ###  EXTERNAL FUNCTION  ### 
def create_spend_chart (categories):
  total = 0
  category_share = []
  for category in categories:
    total += category.withdrawal_counter
  for category in categories:
    calculation = int((category.withdrawal_counter/total)*10)
    category_share.append(calculation)
  
  category_lengths = []
  for category in categories:                                #
    length = len(str(category.category_name))                #calculate max vertical length
    category_lengths.append (length)                         #
  vertical_length = max(category_lengths)

  lines =[]
  i = 0                                                      #
  while i < vertical_length+12:                              # create lines 
    lines.append ('')                                        #
    i += 1

    
  for a in range(11):
    b = 100-a*10
    lines[a] += f'{b}|'.rjust(4)                            #
  lines[11] = '    '                                        # draw chart
  for a in range(vertical_length):                          #
    lines[12+a] += '    '
    
  
  for percentage_spent in category_share:
    
  
    for a in range(11):
      b = 10-a 
      if percentage_spent >= b:                              #
        lines[a] += ' o '                                    # fill percentages / : 
      else:
        lines[a] += '   '
    lines[11] += '---'
  lines[11] += '-'
  for category in categories:
    i = 0                                                    #
    for symbol in list(category.category_name):              # fill category names
      lines[12+i] += f' {symbol} '                           #
      i += 1
    if len(list(category.category_name)) < vertical_length:
      b = vertical_length - len(list(category.category_name))
      for symbol in range(b):
        lines[12+i] += '   '
        i += 1

    
  result= "Percentage spent by category\n"
  for line in lines:
    if '-' in line:
      result += f'{line}\n'
    else:
      result += f'{line} \n'
  result = result[:-1]
  return result
  
    

def display (category_name, ledger, balance): #called by print, might need some work (changed from __str__ to display)
    """External display function"""
    title_line = f'{category_name}'.center (30, "*")
    lines = []
    i = 0
    while i < len(ledger):                                #  
      item = ledger[i]                                    #formatting
      n = len(item['description'])                             #     
      if n > 23:
        n = 23      
      lines.append(str(item['description'])[:23]+"{:.2f}".format(float(item['amount'])).rjust(30-n))
      i+= 1
    result = f'{title_line}\n'
                                                              #
    for x in lines:                                           # result 
      result += f'{x}\n'                                      #
    result += f'Total: {"{:.2f}".format(balance)}'
    
    return result


# Collects values for the chart.js.    
    
def percentage (categories):
  labels = []
  balances = []
  # total_balance ?
  for category in categories:
    labels.append(category.category_name)
    balances.append(category.balance)
  return {'labels':labels, 'balances':balances}