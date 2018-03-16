#!/usr/bin/env python3
"""
requires Python3, validation.py, banking.py, sqlite3

this script provides an interface for creating, accessing, and manipulating customer and account objects.
"""
import base64
import sqlite3
from banking import Account, Customer
import validation
import os


# gets data on customer and initializes customer object
def create_customer():
    clear_output()
    email = validation.required_string("Email:", 25, 0, "[^@]+@[^@]+\.[^@]+")
    if not Customer.is_unique(email):
        print("Email already exists in the database.")
        create_customer()
        return None
    password = validation.required_string("Password: ")
    password = base64.b64encode(password.encode('utf-8'))
    first_name = validation.required_string('First name: ')
    last_name = validation.required_string('Last name: ')
    street_addr = validation.required_string('Street address: ')
    city = validation.required_string('City: ')
    state = validation.required_string('State: ', 2, 2)
    zip = validation.required_string('Zip: ', 5, 5)
    user = Customer(email, password, first_name, last_name, street_addr, city, state, zip)
    account = create_account(user)
    account_menu(user, account)


# gets initial deposit and creates account object
def create_account(user):
    initial_deposit = validation.validate_float("initial deposit amount")
    return Account(user.customer_id, initial_deposit)


# starts chain of events to change active account
def switch_accounts():
    user, account = get_accounts()
    print("Account selected")
    main_menu_prompt(user, account)


# gets a list of accounts in the database and passes it to select_account
def get_accounts():
    accounts_list = Account.get_accounts()
    if accounts_list:
        return select_account(0, 5, accounts_list)
    else:
        print("There are no accounts.")
        input("\nPress enter to return to the account menu: ")
        main_menu()


# takes page, pagesize, and accounts as inputs and presents users a list of accounts to choose from
def select_account(page, pagesize, accounts):
    clear_output()
    start = page * pagesize
    end = (page + 1) * pagesize
    sub_set = accounts[start:end]
    next_page_exists = False
    prev_page_exists = False
    if len(sub_set) == pagesize:
        sub_set.append("Next page")
        next_page_exists = True
    if page > 0:
        sub_set.insert(0, "Previous page")
        prev_page_exists = True
    selection = validation.display_options(sub_set, "Choose an account: ")
    if selection == len(sub_set) and next_page_exists:
        return select_account(page+1, pagesize, accounts)
    if selection == 1 and prev_page_exists:
        return select_account(page - 1, pagesize, accounts)
    account_num = sub_set[selection-1].split(":")[0].split(" ")[1]
    temp_user, temp_account = Account.set_account(account_num)
    return temp_user, temp_account


# presents users with options for their account
def account_menu(user, account):
    clear_output()
    menu = ["Deposit", "Withdraw", "Transfer", "Check Balance", "View Transaction History", "New Account",
            "Select Account", "Quit"]
    print("\n--- Account menu ---\n")
    selection = validation.display_options(menu, "Choose an option: ")
    if selection == 1:
        deposit(user, account, "Deposit")
    elif selection == 2:
        withdraw(user, account, "Withdrawal")
    elif selection == 3:
        transfer(user, account)
    elif selection == 4:
        balance(user, account)
    elif selection == 5:
        transactions(user, account)
    elif selection == 6:
        create_customer()
    elif selection == 7:
        switch_accounts()
    elif selection == 8:
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input")
        account_menu(user, account)


# takes user and account as an input, lets the user deposit funds into the user account
def deposit(user, account, trans_type):
    clear_output()
    amount = validation.validate_float("deposit amount")
    account.deposit(amount, trans_type)
    balance(user, account, True)
    main_menu_prompt(user, account)


# takes user and account as an input, lets the user withdraw funds from the user account
def withdraw(user, account, trans_type, over_min=False):
    if not over_min:
        clear_output()
    amount = validation.validate_float("withdrawal amount")
    if enforce_min(user, account, amount):
        account.withdraw(amount, trans_type)
        balance(user, account, True)
    else:
        withdraw(user, account, trans_type, True)
    main_menu_prompt(user, account)


# takes user, account, and transaction amount as input, prevents user from withdrawing more money than is in the account
def enforce_min(user, account, amount):
    account_balance = account.get_balance()
    if account_balance - amount >= 0:
        return True
    else:
        print("Insufficient funds")
        return False


# takes user and account as input and allows user to transfer funds to another account
def transfer(user, account):
    target_user, target_account = get_accounts()
    if account.account_id == target_account.account_id:
        input("\nYou cannot transfer to the same account, press enter to select a different account")
        transfer(user, account)
    amount = validation.validate_float("withdrawal amount")
    if enforce_min(user, account, amount):
        account.withdraw(amount, "Transfer")
        pass
    else:
        withdraw(user, account, "Transfer")
    target_account.deposit(amount, "Transfer")
    balance(user, account, True)
    main_menu_prompt(user, account)


# takes user, account, and optional boolean as inputs, prints the balance with optional message confirming transaction
def balance(user, account, transaction_check=False):
    clear_output()
    account_balance = account.get_balance()
    if transaction_check:
        print("Your transaction was completed successfully, your new balance is ${:.2f}".format(account_balance))
    else:
        print("Your balance is ${:.2f}".format(account_balance))
        main_menu_prompt(user, account)


# takes user, account, and gets and prints the transaction history for the current account
def transactions(user, account):
    clear_output()
    transaction_list = account.get_transactions()
    for transaction in transaction_list:
        print(transaction)
    main_menu_prompt(user, account)


# takes user, account, and prevents output from being pushed away by the main menu
def main_menu_prompt(user, account):
    input("\nPress enter to return to the account menu: ")
    account_menu(user, account)


# clears previous output
def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')


# presents users with options for creating or accessing an account
def main_menu():
    clear_output()
    menu = ["New Account", "Select Account", "Quit"]
    print("\n--- Main menu ---\n")
    selection = validation.display_options(menu, "Choose an option: ")
    if selection == 1:
        create_customer()
    elif selection == 2:
        switch_accounts()
    elif selection == 3:
        print("Exiting...")
        exit(0)
    else:
        print("Invalid input")
        main_menu()


if __name__ == '__main__':
    main_menu()

