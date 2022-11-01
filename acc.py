class Account:

    def __init__(self, filepath):
        self.path=filepath  #making filepath Global
        with open(filepath,'r') as file:
            self.balance=int(file.read())

    def commit(self):
        with open(self.path,'w') as file:
            file.write(str(self.balance))

    def withdraw(self,amount):
        self.balance=self.balance - amount
        Account.commit(self)
        
    def deposit(self,amount):
        self.balance=self.balance + amount
        Account.commit(self)

class Checking(Account):
    
    type="checking"
    
    def __init__(self,filepath, fee):
        Account.__init__(self, filepath)
        self.fee=fee

    def transfer(self, amount):
        self.balance=self.balance - amount - self.fee
        Account.commit(self)

checking=Checking("balance.txt", 1)
checking.transfer(10)
print(checking.balance)

