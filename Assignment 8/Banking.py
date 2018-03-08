#!/usr/bin/env python3

"""
requires Python3

Script defines and creates a "bank account" which takes an initial balance and allows users to withdraw, deposit, check
balance, and view transaction history.
"""


# define class Account
class Account:
    # initialize account with balance as initial, create empty transaction list, add initial transaction to list
    def __init__(self, initial):
        self.balance = initial
        self.transactions = []
        self.add_transaction(initial,"+")

    # subtracts amount from balance and logs it in transactions
    def withdraw(self, amount):
        self.balance -= amount
        self.add_transaction(amount, "-")

    # adds amount to balance and logs it in transactions
    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(amount, "+")

    # return the balance
    def get_balance(self):
        return self.balance

    # logs the details of a transaction
    def add_transaction(self, amount, symbol):
        log = "Trans #{} \t|\t {}${:.2f} \t|\t Balance: ${:.2f}".format(
            len(self.transactions)+1, symbol, amount, self.get_balance()
        )
        self.transactions.insert(0,log)

    # return transaction list
    def get_transactions(self):
        return self.transactions


