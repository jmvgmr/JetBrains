import random
import sqlite3


class Bank:
    def __init__(self, cursor=None):
        self.accounts = []
        self.cursor = cursor
        cursor.execute('SELECT * FROM card')
        list_card = cursor.fetchall()
        for card in list_card:
            new_account = Account(card[1], card[2])
            self.accounts.append(new_account)

    def create_account(self):
        while True:
            card_number = f'400000{random.randrange(1, 10 ** 9):09}'
            card_number += self.luhn_alg(card_number)
            if card_number not in self.accounts:
                card_pin = f'{random.randrange(1, 10000):04}'
                new_account = Account(card_number, card_pin)
                self.accounts.append(new_account)
                print(f'''
Your card has been created
Your card number:
{card_number}
Your card PIN:
{card_pin}''')
                self.cursor.execute('INSERT INTO card VALUES (?, ?, ?, 0)', (len(self.accounts), card_number, card_pin))
                conn.commit()
                break

    def delete_account(self, account):
        self.accounts.remove(account)
        self.cursor.execute('DELETE FROM card WHERE number = ?', (account.card_number,))
        conn.commit()

    @staticmethod
    def luhn_alg(card_number):
        numbers = list(map(int, card_number))
        for idx, _ in enumerate(numbers):
            if idx % 2 == 0:
                numbers[idx] *= 2
                if numbers[idx] > 9:
                    numbers[idx] -= 9
        checksum = 10 - sum(numbers) % 10
        return str(checksum % 10)

    def credentials_validation(self, card_number, card_pin):
        for account in self.accounts:
            if account.card_number == card_number and account.card_pin == card_pin:
                print('\nYou have successfully logged in!')
                while True:
                    choice = self.log_in()
                    if choice == 0 or choice > 5:
                        return False
                    if choice == 1:
                        print(f'\nBalance: {account.balance}')
                        continue
                    if choice == 2:
                        self.add_income(account)
                        continue
                    if choice == 3:
                        print('\nTransfer')
                        self.transfer(account)
                        continue
                    if choice == 4:
                        self.delete_account(account)
                        return True
                    if choice == 5:
                        print('\nYou have successfully logged out!')
                        return True
        print('\nWrong card number or PIN!')
        return True

    def add_income(self, account):
        amount = int(input('Enter income:\n'))
        account.balance += amount
        self.cursor.execute('UPDATE card SET balance = ? WHERE number = ?', (account.balance, account.card_number))
        conn.commit()
        print('Income was added!')

    def transfer(self, orig_acc):
        dest_acc_num = input('Enter card number:\n')
        for account in self.accounts:
            if account.card_number == dest_acc_num:
                dest_acc = account
            else:
                dest_acc = None
        if dest_acc_num == orig_acc.card_number:
            print('You can\'t transfer money to the same account!')
            return
        elif self.luhn_alg(dest_acc_num[:15]) != dest_acc_num[-1]:
            print('Probably you made mistake in the card number. Please try again!')
            return
        elif not dest_acc:
            print('Such a card does not exist.')
            return
        else:
            amount = int(input('Enter how much money you want to transfer:\n'))
            if amount > orig_acc.balance:
                print('Not enough money!')
                # return
            else:
                orig_acc.balance -= amount
                dest_acc.balance += amount
                self.cursor.execute('UPDATE card SET balance = ? WHERE number = ?', (orig_acc.balance, orig_acc.card_number))
                self.cursor.execute('UPDATE card SET balance = ? WHERE number = ?', (dest_acc.balance, dest_acc.card_number))
                conn.commit()
                print('Success!')
                # return

    @staticmethod
    def log_in():
        print('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
        return int(input())


class Account:
    def __init__(self, card_number, card_pin, balance=0):
        self.card_number = card_number
        self.card_pin = card_pin
        self.balance = balance


def end():
    print('Bye!')


def main(cursor):
    bank = Bank(cursor)
    while True:
        print('''
1. Create an account
2. Log into account
0. Exit''')
        choice = int(input())
        if choice == 1:
            bank.create_account()
        elif choice == 2:
            card_number = input('\nEnter your card number:\n')
            card_pin = input('Enter your PIN:\n')
            if bank.credentials_validation(card_number, card_pin):
                continue
            else:
                end()
                return
        else:
            end()
            return


conn = sqlite3.connect('card.s3db')
# conn = sqlite3.connect(':memory:')

cur = conn.cursor()
try:
    cur.execute('CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
except sqlite3.OperationalError:
    pass

main(cur)
conn.commit()
conn.close()

