#!/usr/bin/env python3
import sys
import os
import time
import sqlite3
import datetime
from tabulate import tabulate
from colorama import Fore,init
import pandas as pd
from sqlalchemy import create_engine
init(autoreset=True)

banner = """
                                                    
             $$$$$$\  $$$$$$\  $$$$$$\ $$\   $$\ $$$$$$\ $$\   $$\$$$$$$$$\ 
            $$  __$$\$$  __$$\$$  __$$\$$ |  $$ $$  __$$\$$ |  $$ \__$$  __|
            $$ /  \__$$ /  $$ $$ /  \__$$ |  $$ $$ /  $$ $$ |  $$ |  $$ |   
            $$ |     $$$$$$$$ \$$$$$$\ $$$$$$$$ $$ |  $$ $$ |  $$ |  $$ |   
            $$ |     $$  __$$ |\____$$\$$  __$$ $$ |  $$ $$ |  $$ |  $$ |   
            $$ |  $$\$$ |  $$ $$\   $$ $$ |  $$ $$ |  $$ $$ |  $$ |  $$ |   
            \$$$$$$  $$ |  $$ \$$$$$$  $$ |  $$ |$$$$$$  \$$$$$$  |  $$ |   
             \______/\__|  \__|\______/\__|  \__|\______/ \______/   \__|   
                                    ATM  SIMULATOR     
                                                                                                                            
"""

connection = sqlite3.connect('ATM.db')
cursor = connection.cursor() # Connection for reading and manipulating database
cnx = create_engine("sqlite:///ATM.db").connect() # SQL Alchemy DB connection for Pandas input(dataframe) which is depended on by Tabulate


# Function to clear CLI screen
def clear():
    os.system('cls')

# Function to print banner
def print_banner(banner_):
    clear()
    banner_ = banner_.split('\n')
    for i in banner_:
        time.sleep(0.01)
        print(Fore.GREEN +i)
    print(Fore.RESET + '\n\n\n')

# Function to print string line by line slowly
def fancy_print(arr):
    for i in arr:
        time.sleep(0.1)
        print(i)

def authenticate(pin):
    pin_trials = 1
    while pin_trials <= 4:
        pin_input = input(f"Enter your ATM PIN ({pin}): ")
        if pin_input == str(pin) or pin_input == "":
            clear()
            load_menu()
        else:
            print(f'{Fore.RED}PIN Incorrect (Enter "{pin}")\n')
            pin_trials += 1
    print("PIN Trials exceeded!")
    time.sleep(1.1)
    main()

class Account:
    def __init__(self,id_):
        self.account = cursor.execute("SELECT * FROM accounts WHERE account_id=:id",{'id':id_}).fetchone()
        self.account_id = self.account[0]
        self.account_balance = self.account[1]
        self.account_pin = self.account[2]
        self.account_name = self.account[3]
        self.account_type = self.account[4]
        self.account_number = self.account[5]

    def get_account(self):
        return self.account

    def get_id(self):
        return self.account_id
    
    def get_balance(self):
        return self.account_balance
    
    def get_pin(self):
        return self.account_pin
    
    def get_name(self):
        return self.account_name
    
    def get_type(self):
        return self.account_type
    
    def get_account_number(self):
        return self.account_number


def generate_receipt(receipt_info):
    print('\n\n')
    print(f"{'RECEIPT': ^34}")
    print(tabulate(receipt_info, tablefmt='grid'))
    customer_name = receipt_info[0][1]
    curr_time = receipt_info[3][1]
    with open('Receipt for '+customer_name+' ' +str(curr_time.split(':')[1])+'.txt', 'w', encoding='utf8') as output:
        output.write(f"{'Receipt': ^34}\n")
        output.write(tabulate(receipt_info, tablefmt='grid'))


def withdraw():
    clear()
    account = cursor.execute("SELECT * FROM accounts WHERE account_id=6").fetchone()
    # print(account)
    account_id = account[0]
    account_balance = account[1]
    account_name = account[3]
    print(f"\n{Fore.YELLOW}WELCOME {account_name.upper()}{Fore.RESET}")
    fancy_print("WITHDRAWAL MENU: \n\n1. N1,000\n\n2. N3,000\n\n3. N5,000\n\n4. N10,000\n\n5. N20,000\n\n6. Other amount\n".split('\n'))
    

    def withdraw_amount(amount_):
        if account_balance >= amount_:
            new_balance = account_balance - amount_
            date = datetime.date.today()
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            cursor.execute("UPDATE accounts SET account_balance=:new_balance WHERE account_id=6",{'new_balance': new_balance})
            connection.commit()
            receipt_info = [['Customer', account_name], ['Withdrawal amount', 'N' +str(amount_)], ['Date', date], ["Time", curr_time]]
            generate_receipt(receipt_info)
            print(f"\n\n{Fore.GREEN}Withdrawal Successful!{Fore.RESET}")
            time.sleep(2)
        else:
            print("Insufficient balance")

    while True:
        option = input(f"{Fore.GREEN}Select amount to withdraw: {Fore.RESET}")
        if option == '1':
            withdraw_amount(1000)
            return
        elif option == '2':
            withdraw_amount(3000)
            return
        elif option == '3':
            withdraw_amount(5000)
            return
        elif option == '4':
            withdraw_amount(10000)
            return
        elif option == '5':
            withdraw_amount(20000)
            return
        elif option == '6':
            clear()
            while True:
                amount = input(f"\n\n{Fore.YELLOW}Enter preferred amount(Greater than 1000 and Less than 20000): {Fore.RESET}")
                if amount.strip(',').isdigit():
                    amount = int(amount.strip(','))
                    if amount <= 20000 and int(amount) >= 1000:
                        withdraw_amount(amount)
                        return
                    else:
                        print(f"\n{Fore.RED}Invalid amount{Fore.YELLOW}(Enter between 1000 and 20000){Fore.RESET}\n")
                else:
                    print(f"\n{Fore.RED}Invalid input{Fore.YELLOW}(Enter a digit){Fore.RESET}")
        else:
            print(f"\n{Fore.RED}Invalid input{Fore.YELLOW}(Enter between 1 - 6){Fore.RESET}")

def transfer():
    clear()
    account_balance = cursor.execute("SELECT account_balance FROM accounts WHERE account_id=6").fetchone()[0]
    other_accounts = pd.read_sql_query("SELECT * FROM accounts WHERE account_id != 6", cnx)
    other_accounts.set_index('account_id', inplace=True)
    other_accounts_for_tabulate = pd.read_sql_query("SELECT account_id, account_name, account_type, account_number FROM accounts WHERE account_id != 6", cnx)
    other_accounts_for_tabulate.set_index('account_id', inplace=True)
    print()
    print(f"{'AVAILABLE RECEIVING ACCOUNTS': ^80}")
    fancy_print(tabulate(other_accounts_for_tabulate, headers='keys', tablefmt='fancy_grid').split('\n'))
    while True:
        other_account_id = int(input(f"\n\n{Fore.YELLOW}Enter account ID of account you're transfering funds to: {Fore.RESET}"))
        if other_account_id in other_accounts.index.tolist():
            other_account_name = other_accounts.loc[other_account_id, 'account_name']
            other_account_number = other_accounts.loc[other_account_id, 'account_number']
            other_account_type = other_accounts.loc[other_account_id, 'account_type']
            other_account_balance = other_accounts.loc[other_account_id, 'account_balance']
            
            while True:
                transfer_amount = input(f"\n{Fore.YELLOW}Enter transfer amount: {Fore.RESET}")
                if transfer_amount.isdigit():
                    transfer_amount = float(transfer_amount)
                    if transfer_amount < account_balance:
                        print(f"\n\n{Fore.BLUE}RECEIPIENT:\n\nName: {other_account_name}\n\nAccount number: {other_account_number}\n\nAccount type: {other_account_type.upper()}\n\nAmount: N{transfer_amount:,}{Fore.RESET}\n\n")
                        enter = input(f"{Fore.YELLOW}Hit enter to complete transfer...{Fore.RESET}")

                        new_balance = float(account_balance - transfer_amount)
                        other_new_balance = float(other_account_balance + transfer_amount)

                        cursor.execute("UPDATE accounts SET account_balance=:new_balance WHERE account_id=6", {'new_balance': new_balance})
                        cursor.execute("UPDATE accounts SET account_balance=? WHERE account_id=?", (other_new_balance, other_account_id))
                        connection.commit()

                        print(f"\n\n{Fore.GREEN}Yay! You successfully transferred N{transfer_amount:,} to {other_account_name}{Fore.RESET}")
                        return
                    else:
                        print("Enter amount smaller than balance.")
                    
                else:
                    print("\nIncorrect format(Only digits are allowed)\n")
        else:
            print(f"\n{Fore.RED}Invalid input({Fore.RESET}Enter an ID from the list{Fore.RED}){Fore.RESET}")


def get_balance():
    clear()
    account = cursor.execute("SELECT * FROM accounts WHERE account_id=6").fetchone()
    account_name = account[3]
    account_balance = account[1]
    print(f"\n\n{Fore.YELLOW}Dear {account_name.upper()} your account balance is {Fore.RESET}N{account_balance:,}")
    return

def make_deposit():
    clear()
    account_balance = cursor.execute("SELECT account_balance FROM accounts WHERE account_id=6").fetchone()[0]
    while True:
        deposit_amount = input(f"\n{Fore.YELLOW}Enter deposit amount: {Fore.RESET}")
        if deposit_amount.isdigit():
            deposit_amount = float(deposit_amount)
            # print(f"\n\n{Fore.BLUE}RECEIPIENT:\n\nName: {other_account_name}\n\nAccount number: {other_account_number}\n\nAccount type: {other_account_type}\n\nAmount: N{transfer_amount:,}{Fore.RESET}\n\n")
            print(f"\n\n{Fore.BLUE}Make a deposit of N{deposit_amount:,} to your account\n\nCurrent Balance: N{account_balance:,}\n{Fore.RESET}")
            enter = input(f"{Fore.YELLOW}Hit enter to complete deposit...{Fore.RESET}")

            new_balance = float(account_balance + deposit_amount)

            cursor.execute("UPDATE accounts SET account_balance=:new_balance WHERE account_id=6", {'new_balance': new_balance})
            connection.commit()

            print(f"\n{Fore.GREEN}Yay! You successfully deposited N{deposit_amount:,} to your account.{Fore.RESET}\n\nNew account balance: N{new_balance:,}\n")
            return
            
        else:
            print(f"\n{Fore.RED}Incorrect format{Fore.YELLOW}(Only digits are allowed){Fore.RESET}\n")


def change_pin():
    clear()
    pin = cursor.execute("SELECT account_pin FROM accounts WHERE account_id=6").fetchone()[0]
    pin_trials = 1
    while pin_trials <= 4:
        pin_input = input(f"\n{Fore.YELLOW}Enter your current ATM PIN ({pin}): ")
        if pin_input == str(pin):
            while True:
                new_pin = input(f"\n{Fore.YELLOW}Enter your new ATM PIN (4 DIGITS): ")
                if new_pin.isdigit():
                    if len(new_pin) == 4:
                        enter = input(f"\n{Fore.YELLOW}Hit enter to change current PIN now...{Fore.RESET}")
                        cursor.execute("UPDATE accounts SET account_pin=:new_pin WHERE account_id=6",{'new_pin':new_pin})
                        connection.commit()
                        print(f"\n{Fore.GREEN}Congratulations! You've successfully changed your ATM PIN.{Fore.RESET}")
                        return
                    else:
                        print(f"{Fore.RED}Invalid format(Enter a 4 digit number){Fore.RESET}")
                else:
                    print(f"{Fore.RED}Invalid format(Enter a digit){Fore.RESET}")
        else:
            print(f'\n{Fore.RED}PIN Incorrect (Enter "{pin}")\n')
            pin_trials += 1
        
    print("PIN Trials exceeded!")
    time.sleep(1.1)
    main()

def load_menu():
    while True:
        fancy_print("\n ACCOUNT OPTIONS: \n\n 1. WITHDRAWAL \n\n 2. TRANSFER \n\n 3. CHECK BALANCE \n\n 4. MAKE DEPOSIT\n\n 5. CHANGE PIN\n".split('\n'))
        option = input(f"{Fore.YELLOW} Select preferred option: {Fore.RESET}")
        if option == '1':
            withdraw()
            enquire()
        elif option == '2':
            transfer()
            enquire()
        elif option == '3':
            get_balance()
            enquire()
        elif option == '4':
            make_deposit()
            enquire()
        elif option == '5':
            change_pin()
            enquire()
        else:
            print(f"\n{Fore.RED}Invalid input(Enter between 1 - 5){Fore.RESET}")

def enquire():
    while True:
        # clear()
        # print('\n'+ '#'*20)
        fancy_print("\nWould you like to make another transaction?\n1. Yes\n2. No\n".split('\n'))
        option = input(f"{Fore.YELLOW}Enter preferred option: {Fore.RESET}")
        if option == '1':
            main()
        elif option == '2':
            print('\n\nThank You for banking with Us!', end='')
            for i in '....':
                time.sleep(0.5)
                print(i, end='')
            clear()
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}Invalid input (Enter 1 or 2){Fore.RESET}")

def main():
    clear()
    print_banner(banner)
    cursor.execute("SELECT account_pin FROM accounts WHERE account_id=6")
    pin = cursor.fetchone()[0]
    authenticate(pin)

if __name__ == '__main__':
    # main()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Execution Interrupted!{Fore.RESET}")
        time.sleep(0.2)
        clear()
        sys.exit(0)
