import random
import os
import yaml
import argparse

code = "abcdefghijklmnopqrstuvwxyz0123456789"

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    # def deposit(self,  amount):
    #     self.balance += amount

    # def withdraw(self, amount):
    #     if self.balance - amount < 0:
    #         print("Can't withdraw money")
    #         return
    #     self.balance -= amount

    def get_balance(self):
        print(self.balance)
        return self.balance


class Client():

    def __init__(self, account_path, client_id=None):
        self.account_id = []
        self.bank_accounts = []
        self.num_accounts = 0
        self.account_path = account_path

        if os.path.exists(account_path):
            with open(self.account_path, 'r') as file:
                self.account_dict = yaml.full_load(file)
                self.client_id = client_id
            if self.client_id in self.account_dict.keys():
                self.num_accounts = len(self.account_dict[self.client_id])
                self.account_id.extend(self.account_dict[self.client_id])
                self.bank_accounts.extend(self.account_dict[self.client_id])
            elif self.client_id == None:
                balance = int(input("How much money to add to account: "))
                self.client_id = ''
                for i in range(8):
                    self.client_id += random.choice(code)
                self.add_bank_account(balance)
                self.account_dict.update({self.client_id : i for i in self.bank_accounts})
                with open(self.account_path, "a") as file:
                    yaml.dump({self.client_id : [i for i in self.bank_accounts]}, file)
            else:
                balance = int(input("How much money to add to account: "))
                self.add_bank_account(balance)
                self.account_dict.update({self.client_id : i for i in self.bank_accounts})
                with open(self.account_path, "a") as file:
                    yaml.dump({self.client_id : [i for i in self.bank_accounts]}, file)

        else:
            if client_id == None:
                balance = int(input("How much money to add to account: "))
                self.add_bank_account(balance)  
                self.client_id = ""
                for i in range(8):
                    self.client_id += random.choice(code)
                self.account_dict = {self.client_id:self.bank_accounts[0]}
                with open(account_path, "w") as fw:
                    yaml.dump(self.account_dict, fw)
            else:
                balance = int(input("How much money to add to account: "))
                self.add_bank_account(balance)  
                self.client_id = client_id
                self.account_dict = {self.client_id:self.bank_accounts[0]}
                with open(account_path, "w") as fw:
                    yaml.dump(self.account_dict, fw)

    def add_bank_account(self, amount, mod=False, account_id=None):
        b = BankAccount(amount)

        account_id = ''
        account_id = random.randint(100000, 999999)
        self.account_id.append(account_id)
        self.bank_accounts.append({self.account_id[self.num_accounts]: b.balance})
        self.num_accounts += 1

        print("Account id: " + str(account_id))

        if mod:
            with open(self.account_path, "r") as fr:

                self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
                self.account_dict[self.client_id] = self.bank_accounts

                with open(self.account_path, "w") as fw:
                    yaml.dump(self.account_dict, fw)

    def deposit(self, amount, account_id, importance = "Primary"): 
        if not self.bank_accounts:
            raise ValueError("No bank accounts")
        with open(self.account_path, "r") as fr:
            self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
        if len(self.account_dict[self.client_id]) > 1:
            for y in range(0, self.num_accounts):
                for i in self.account_dict[self.client_id][y].keys():
                    if i == account_id:
                        self.account_dict[self.client_id][y][account_id] += amount
                    break
        else:
            if importance == "Primary":
                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id]:
                        if i == account_id:
                            self.account_dict[self.client_id][account_id] += amount
                        break
            else:
                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id][0].keys():
                        if i == account_id:
                            self.account_dict[self.client_id][0][i] += amount
                        break
        with open(self.account_path, "w") as fw:
            yaml.dump(self.account_dict, fw)

    def withdraw(self, amount, account_id, importance = "Primary"):
        if not self.bank_accounts:
            raise ValueError("No bank accounts")
        with open(self.account_path, "r") as fr:
            self.account_dict = yaml.load(fr, Loader=yaml.FullLoader)
        if len(self.account_dict[self.client_id]) > 1:
            for y in range(0, self.num_accounts):
                for i in self.account_dict[self.client_id][y].keys():
                    if i == account_id:
                        if amount > self.account_dict[self.client_id][y][account_id]:
                            raise ValueError("Not enought money")
            for y in range(0, self.num_accounts):
                for i in self.account_dict[self.client_id][y].keys():
                    if i == account_id:
                        self.account_dict[self.client_id][y][account_id] -= amount
                    break
        else: 
            if importance == "Primary":
                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id]:
                        if i == account_id:
                            if amount > self.account_dict[self.client_id][account_id]:
                                raise ValueError("Not enought money")

                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id]:
                        if i == account_id:
                            self.account_dict[self.client_id][account_id] -= amount
                        break
            else:
                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id][0].keys():
                        if i == account_id:
                            if amount > self.account_dict[self.client_id][0][i]:
                                raise ValueError("Not enought money")

                for y in range(0, self.num_accounts):
                    for i in self.account_dict[self.client_id][0].keys():
                        if i == account_id:
                            self.account_dict[self.client_id][0][i] -= amount
                        break

        with open(self.account_path, "w") as fw:
            yaml.dump(self.account_dict, fw)

    def transfer(self, account1_id, client, account2_id, amount, operation="deposit"):
        if not isinstance(client, Client):
            print("Not a client")
            return
        if operation == "deposit":
            client.withdraw(amount, account2_id, "Secondary")
            with open(self.account_path, "r") as fr:
                self.account_dict = yaml.full_load(fr)
            self.deposit(amount, account1_id, "Primary")
        elif operation == "withdraw":
            with open(self.account_path, "r") as fr:
                self.account_dict = yaml.full_load(fr)
            self.withdraw(amount, account1_id, "Primary")
            client.deposit(amount, account2_id, "Secondary")
        else:
            raise ValueError("No such function")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename', required=True,
                        help='Path to file')
    parser.add_argument('-a', action='store', dest='action_to_take', required=False,
                        help='Deposit/Withdraw/Transfer/Add_account to file', default="add_account")
    parser.add_argument('-id', action='store', dest='id', required=False,
                        help='Your id', default=None)

    options = parser.parse_args()
    FILE_PATH = options.filename
    ID1 = options.id

    client1 = Client(FILE_PATH, ID1)

    if options.action_to_take == 'deposit':
        ID_ACCOUNT1 = int(input("To which of your accounts do you wish to deposit: "))
        amount = int(input("How much do you wish to deposit: "))
        client1.deposit(amount, ID_ACCOUNT1)
    elif options.action_to_take == 'withdraw':
        ID_ACCOUNT1 = int(input("From which of your accounts do you wish to withdraw: "))
        amount = int(input("How much do you wish to withdraw: "))
        client1.withdraw(amount, ID_ACCOUNT1)
    elif options.action_to_take == 'transfer':
        ID2 = input("To/From which client do you wish to transfer money: ")
        if ID2 == "None":
            client2 = Client(FILE_PATH)
        else:
            client2 = Client(FILE_PATH, ID2)
        ID_ACCOUNT2 = int(input("To/From which account do you wish to transfer money: "))
        ID_ACCOUNT1 = int(input("To/From which of your accounts do you wish to transfer money: "))
        action = input("Do you wish to deposit to or withdraw from the first account: ")
        amount = int(input(f"How much do you wish to {action}: "))
        client1.transfer(ID_ACCOUNT1, client2, ID_ACCOUNT2, amount, action)
    elif options.action_to_take == 'add_account':
        amount = int(input("How much money do you wish to add to the new acount: "))
        client1.add_bank_account(amount, True)