import math
import argparse


class CreditCalculator:
    def __init__(self):
        self.type = None
        self.credit_principal = 0
        self.monthly_payment = 0.0
        self.credit_interest = 0.0
        self.month_count = 0

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--type")
        parser.add_argument("--payment", type=float)
        parser.add_argument("--principal", type=int)
        parser.add_argument("--periods", type=int)
        parser.add_argument("--interest", type=float)
        args = parser.parse_args()

        arg_count = 0
        if args.type:
            self.type = args.type
            arg_count += 1

        if args.payment:
            self.monthly_payment = args.payment
            arg_count += 1

        if args.principal:
            self.credit_principal = args.principal
            arg_count += 1

        if args.periods:
            self.month_count = args.periods
            arg_count += 1

        if args.interest:
            self.credit_interest = args.interest
            arg_count += 1

        if arg_count < 4 \
            or not args.type \
            or args.type not in ("annuity", "diff") \
            or (self.type == "diff" and args.payment) \
            or not args.interest \
            or self.monthly_payment < 0 \
            or self.credit_principal < 0 \
            or self.month_count < 0 \
            or self.credit_interest < 0:
            print("Incorrect parameters.")

        if self.type == "diff":
            self.get_calculated_differential_payments()
        else:
            if not args.payment:
                self.get_calculated_monthly_payment()
            elif not args.principal:
                self.get_calculated_credit_principal()
            elif not args.periods:
                self.get_calculated_month_count()

    def get_nominal_interest_rate(self):
        return self.credit_interest / (12 * 100)

    def get_calculated_differential_payments(self):
        nominal_rate = self.get_nominal_interest_rate()

        i = 1
        total = 0
        while i <= self.month_count:
            month_payment = (self.credit_principal / self.month_count) + (nominal_rate * (self.credit_principal - ((self.credit_principal * (i - 1)) / self.month_count)))

            if round(month_payment) < month_payment:
                month_payment += 1

            month_payment = round(month_payment)
            total += month_payment

            print("Month {}: paid out {}".format(i, month_payment))

            i += 1

        if total > self.credit_principal:
            print("Overpayment = {}".format(total - self.credit_principal))

    def get_calculated_month_count(self):
        nominal_rate = self.get_nominal_interest_rate()

        if (self.monthly_payment - (nominal_rate * self.credit_principal)) == 0 or nominal_rate == 0.0:
            print("Incorrect parameters.")
        else:
            n = math.log(self.monthly_payment / (self.monthly_payment - (nominal_rate * self.credit_principal)), 1 + nominal_rate)
            if n % 2 != 0:
                n = int(n + 1)

            if n < 12:
                print("You need {} months to repay this credit!".format(n))
            elif n == 12:
                print("You need 1 year to repay this credit!")
            else:
                years = n // 12
                months = n % 12
                print("You need {} years and {} months to repay this credit!".format(years, months))

            total = self.monthly_payment * n
            if total > self.credit_principal:
                print("Overpayment = {}".format(total - self.credit_principal))

    def get_calculated_monthly_payment(self):
        nominal_rate = self.get_nominal_interest_rate()
        n = self.credit_principal * ((nominal_rate * math.pow((1 + nominal_rate), self.month_count)) / (math.pow((1 + nominal_rate), self.month_count) - 1))
        if n % 2 != 0:
            n += 1

        annuity_payment = round(n)
        print("Your annuity payment = {}!".format(annuity_payment))

        total = annuity_payment * self.month_count
        if total > self.credit_principal:
            print("Overpayment = {}".format(total - self.credit_principal))

    def get_calculated_credit_principal(self):
        nominal_rate = self.get_nominal_interest_rate()
        p = self.monthly_payment / ((nominal_rate * math.pow((1 + nominal_rate), self.month_count)) / (math.pow((1 + nominal_rate), self.month_count) - 1))
        credit_principal = round(p)

        print("Your credit principal = {}!".format(credit_principal))

        total = self.monthly_payment * self.month_count
        if total > credit_principal:
            print("Overpayment = {}".format(total - credit_principal))


calculator = CreditCalculator()
calculator.run()
