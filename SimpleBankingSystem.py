import random
import sqlite3


def check_luhn(credit_card_number: str):
    number = [int(x) for x in credit_card_number]
    for i in range(16):
        if i % 2 != 0:
            number[i - 1] = number[i - 1] * 2

    for i in range(16):
        value = number[i - 1]
        if value > 9:
            number[i - 1] = value - 9

    total = 0
    for i in range(16):
        total += number[i]

    return total % 10 == 0


class BankingSystem:
    def __init__(self):
        self.valid_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.conn = sqlite3.connect("card.s3db")

        cursor = self.conn.cursor()
        cursor.execute("drop table card")
        cursor.execute("create table card (id integer primary key, number text, pin text, balance integer default 0)")

    def create_account(self):
        credit_card_number = [4, 0, 0, 0, 0, 0]
        for i in range(9):
            credit_card_number.append(random.choice(self.valid_numbers))

        credit_card_number_checksum = credit_card_number.copy()

        # compute checksum
        for i in range(16):
            if i % 2 != 0:
                credit_card_number_checksum[i - 1] = credit_card_number_checksum[i - 1] * 2

        for i in range(15):
            value = credit_card_number_checksum[i - 1]
            if value > 9:
                credit_card_number_checksum[i - 1] = value - 9

        total = 0
        for i in range(15):
            total += credit_card_number_checksum[i - 1]

        if total % 10 == 0:
            credit_card_number.append(0)
        else:
            for i in range(10):
                if (total + i) % 10 == 0:
                    credit_card_number.append(i)
                    break

        credit_card_number_string = str(credit_card_number).replace("[", "").replace("]", "").replace(",", "").replace(" ", "")

        # get PIN
        pin = ""
        for i in range(4):
            pin += str(random.choice(self.valid_numbers))

        cursor = self.conn.cursor()
        cursor.execute("insert into card (number, pin) values ({}, {})".format(credit_card_number_string, pin))
        self.conn.commit()

        print("Your card has been created")
        print("Your card number:\n{}".format(credit_card_number_string))
        print("Your card PIN:\n{}".format(pin))

    def login(self):
        print("Enter your card number:")
        credit_card_number = int(input())

        print("Enter your PIN:")
        pin = int(input())

        cursor = self.conn.cursor()
        cursor.execute("select id from card where number = '{}' and pin = '{}'".format(credit_card_number, pin))
        row_id = cursor.fetchone()

        if row_id is not None:
            print("You have successfully logged in!")

            return self.logged_in(row_id[0])
        else:
            print("Wrong card number or PIN!")

        return True

    def logged_in(self, row_id):
        print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")

        option = int(input())
        while option in (1, 2, 3, 4):
            cursor = self.conn.cursor()

            if option == 1:
                cursor.execute("select balance from card where id = {}".format(row_id))
                balance = cursor.fetchone()

                print("Balance: {}".format(balance))
            elif option == 2:
                print("Enter income:")
                income = int(input())

                cursor.execute("update card set balance = balance + {} where id = {}".format(income, row_id))
                self.conn.commit()

                print("Income was added!")
            elif option == 3:
                print("Transfer")
                print("Enter card number:")
                credit_card_number = input()
                if check_luhn(credit_card_number):
                    cursor.execute("select id from card where number = '{}'".format(credit_card_number))
                    transfer_to_row_id = cursor.fetchone()

                    if transfer_to_row_id is not None:
                        print("Enter how much money you want to transfer:")
                        amount = int(input())

                        cursor.execute("select balance from card where id = {}".format(row_id))
                        account_balance = cursor.fetchone()

                        if amount < account_balance[0]:
                            cursor.execute("update card set balance = balance - {} where id = {}".format(amount, row_id))
                            cursor.execute("update card set balance = balance + {} where id = {}".format(amount, transfer_to_row_id[0]))
                            self.conn.commit()

                            print("Success!")
                        else:
                            print("Not enough money!")
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made mistake in the card number. Please try again!")
            elif option == 4:
                cursor.execute("delete from card where id = {}".format(row_id))
                self.conn.commit()

                print("The account has been closed!")
                break

            option = int(input())

        if option == 5:
            print("You have successfully logged out!")

            return True
        elif option == 0:
            return False

        return self.logged_in(row_id)

    def run(self):
        print("1. Create an account\n2. Log into account\n0. Exit")
        option = int(input())

        if option == 1:
            self.create_account()
            return True
        elif option == 2:
            return self.login()

        return False


banking_system = BankingSystem()
run = banking_system.run()
while run:
    run = banking_system.run()

print("Bye!")
