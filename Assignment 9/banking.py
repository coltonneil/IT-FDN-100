#!/usr/bin/env python3
"""
requires Python3

Script defines the Customer class and inserts it into a DB it also creates the bank account class which takes an
initial balance and allows users to withdraw, deposit, check balance, and view transaction history.
"""
import sqlite3

connection = sqlite3.connect('Bank.db')
# an empty DB for demonstration purposes
# connection = sqlite3.connect('Bank_Empty.db')


# define customer class
class Customer:
    def __init__(self, email, password, first_name, last_name, street_addr, city, state, zip, customer_id=""):
        self.customer_id = customer_id
        self.email = email.lower()
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.street_addr = street_addr
        self.city = city
        self.state = state
        self.zip = zip
        if customer_id == "":
            self.insert()

    # insert customer into DB
    def insert(self):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers "
                       "(email,password,first_name,last_name,street_addr,city,state,zip) "
                       "VALUES (?,?,?,?,?,?,?,?)",
                       (self.email, self.password, self.first_name,
                        self.last_name, self.street_addr, self.city, self.state, self.zip))
        connection.commit()
        record_set = cursor.execute("SELECT customer_id FROM customers WHERE email=?", (self.email,))
        self.customer_id = record_set.fetchone()[0]

    # check is email is in DB
    @staticmethod
    def is_unique(email):
        cursor = connection.cursor()
        record_set = cursor.execute("SELECT customer_id FROM customers WHERE email=?", (email.lower(),))
        if record_set.fetchone():
            return False
        else:
            return True


# define class Account
class Account:
    # initialize account with balance as initial, create empty transaction list, add initial transaction to list
    def __init__(self, customer_id, initial, account_id="", transactions=[]):
        self.account_id = account_id
        self.customer_id = customer_id
        self.transactions = transactions
        self.balance = 0
        if self.account_id == "":
            self.transactions = []
            self.deposit(initial, "Initial")
            self.insert()
        else:
            self.balance = initial
            self.transactions = transactions

    # insert account into DB
    def insert(self):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts "
                       "(customer_id, balance, transactions) "
                       "VALUES (?,?,?)",
                       (self.customer_id, self.balance, ','.join(self.transactions)))
        connection.commit()
        record_set = cursor.execute("SELECT account_id FROM accounts WHERE customer_id=?", (self.customer_id,))
        self.account_id = record_set.fetchone()[0]

    # update account in DB
    def update(self):
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts "
                       "SET balance = ? , transactions = ? "
                       "WHERE customer_id = ?",
                       (self.balance, ','.join(self.transactions), self.customer_id))
        connection.commit()

    # subtracts amount from balance and logs it in transactions
    def withdraw(self, amount, trans_type):
        self.balance -= amount
        self.add_transaction(amount, "-", trans_type)
        self.update()

    # adds amount to balance and logs it in transactions
    def deposit(self, amount, trans_type):
        self.balance += amount
        self.add_transaction(amount, "+", trans_type)
        self.update()

    # return the balance
    def get_balance(self):
        return self.balance

    # logs the details of a transaction
    def add_transaction(self, amount, symbol, trans_type):
        log = "Trans #{} \t|\t {} \t|\t {}${:.2f} \t|\t Balance: ${:.2f}".format(
            len(self.transactions)+1, trans_type, symbol, amount, self.get_balance()
        )
        for transaction in self.transactions:
            print(transaction)
        self.transactions.insert(0, log)
        with open("transaction_log.txt", "a") as output:
            output.write("Account ID:{} - LOG:{}".format(self.account_id, log))

    # return transaction list
    def get_transactions(self):
        return self.transactions

    # return list of all accounts formatted as strings
    @staticmethod
    def get_accounts():
        cursor = connection.cursor()
        record_set = cursor.execute("SELECT A.account_id, C.first_name, C.last_name, A.balance "
                                    "FROM customers C "
                                    "INNER JOIN accounts A "
                                    "ON C.customer_id = A.customer_id")
        accounts_rs = record_set.fetchall()
        if not accounts_rs:
            return False
        else:
            account_list = []
            for record in accounts_rs:
                account_number = record[0]
                first_name = record[1]
                last_name = record[2]
                balance = record[3]
                account_info = "Account {}: {} {} - {}".format(account_number, first_name, last_name, balance)
                account_list.append(account_info)
            return account_list

    # initialize a customer and account using data from the DB
    @staticmethod
    def set_account(account_number):
        cursor = connection.cursor()
        record_set = cursor.execute("SELECT C.customer_id, C.email, C.password, C.first_name, C.last_name, "
                                    "C.street_addr, C.city, C.state, C.zip, A.account_id, A.balance, A.transactions "
                                    "FROM customers C "
                                    "INNER JOIN accounts A "
                                    "ON C.customer_id = A.customer_id "
                                    "WHERE A.account_id = ?", (account_number,))
        account_rs = record_set.fetchone()
        if not account_rs:
            return False
        else:
            user = Customer(account_rs[1], account_rs[2], account_rs[3], account_rs[4], account_rs[5], account_rs[6],
                            account_rs[7], account_rs[8], account_rs[0])
            transactions = account_rs[11].split(",")
            account = Account(account_rs[0], account_rs[10], account_rs[9], transactions)
            return user, account
