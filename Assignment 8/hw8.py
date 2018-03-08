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


# presents users with options for thier account
def main_menu(account):
    menu = ["Deposit", "Withdraw", "Check Balance", "View Transaction History", "Quit"]
    print("\n--- Main menu ---\n")
    selection = display_options(menu, "Choose an option: ")
    print(selection)
    if selection == 1:
        deposit(account)
    elif selection == 2:
        withdraw(account)
    elif selection == 3:
        balance(account)
    elif selection == 4:
        transactions(account)
    elif selection == 5:
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input")
        main_menu()


# takes user account as an input, lets the user deposit funds into the user account
def deposit(user_account):
    amount = validate_float("deposit amount")
    user_account.deposit(amount)
    balance(user_account, True)
    main_menu_prompt(user_account)


# takes user account as an input, lets the user withdraw funds from the user account
def withdraw(user_account):
    amount = validate_float("withdraw amount")
    if enforce_min(user_account, amount):
        user_account.withdraw(amount)
        balance(user_account, True)
    else:
        withdraw(user_account)
    main_menu_prompt(user_account)


# user account and transaction amount as input, prevents user from withdrawing more money than is in the account
def enforce_min(user_account, amount):
    account_balance = user_account.get_balance()
    if account_balance - amount >= 0:
        return True
    else:
        print("Insufficient funds")
        return False


# user account and optional boolean as inputs, prints the account balance with optional message confirming transaction
def balance(user_account, transaction_check=False):
    account_balance = user_account.get_balance()
    if transaction_check:
        print("Your transaction was completed successfully, your new balance is ${:.2f}".format(account_balance))
    else:
        print("Your balance is ${:.2f}".format(account_balance))
        main_menu_prompt(user_account)


# get and print the transaction history for the current account
def transactions(user_account):
    transaction_list = user_account.get_transactions()
    for transaction in transaction_list:
        print(transaction)
    main_menu_prompt(user_account)


# builds a menu from an array or dictionary and presents the user with a numeric choice, returns that selection
def display_options(options, prompt):
    lookup_dict = {}
    for index, item in enumerate(options):
        print("[{}] - {}".format(str(index + 1), item))
        if type(options) == dict:
            lookup_dict[index + 1] = item
    while True:
        try:
            selection = int(input(prompt))
        except ValueError:
            print("Selection must be a number")
            continue
        if selection < 1 or selection > len(options) + 1:
            print("Choose a number from the list")
            continue
        else:
            break
    if type(options) == dict:
        return lookup_dict[selection]
    else:
        return selection


# gets and validates floats
def validate_float(data_name, allow_zero=False):
    while True:
        try:
            tmp_float = float(input("Input {}: ".format(data_name)))
        except ValueError:
            print("{} must be a number".format(data_name))
            continue
        if tmp_float < 1 and not allow_zero:
            print("{} must be greater than 0".format(data_name))
            continue
        else:
            break
    return round(tmp_float, 2)


# prevents output from being pushed away by the main menu by asking the user to press a key to continue
def main_menu_prompt(user_account):
    input("\nPress any key to return to the main menu: ")
    main_menu(user_account)


# gets initial deposit and creates account object
def create_account():
    initial_deposit = validate_float("initial deposit amount")
    user_account = Account(initial_deposit)
    main_menu(user_account)


create_account()
