import math
import argparse


def count_months(cred_prin, mont_paym, cred_inte):
    interest_rate = cred_inte / (12 * 100)
    n = math.log(mont_paym / (mont_paym - interest_rate * cred_prin), 1 + interest_rate)
    n = math.ceil(n)
    n_years = n // 12
    plural_y = 's' if n_years != 1 else ''
    if n % 12:
        n_months = n % 12
        plural_m = 's' if n_months != 1 else ''
        print(f'You need {n // 12} year{plural_y} and {n % 12} month{plural_m} to repay this credit!')
    else:
        print(f'You need {n // 12} year{plural_y} to repay this credit!')
    overpayment(cred_prin, mont_paym, n)


def annuity_monthly_payment(cred_prin, n_per, cred_inte):
    interest_rate = cred_inte / (12 * 100)
    mon_pay = cred_prin * (interest_rate * math.pow(1 + interest_rate, n_per)) / (math.pow(1 + interest_rate, n_per) - 1)
    mon_pay = math.ceil(mon_pay)
    print(f'Your annuity payment = {mon_pay}!')
    overpayment(cred_prin, mon_pay, n_per)


def credit_principal(mon_pay, n_per, cred_inte):
    interest_rate = cred_inte / (12 * 100)
    cred_prin = mon_pay / ((interest_rate * (1 + interest_rate) ** n_per) / ((1 + interest_rate) ** n_per - 1))
    print(f'Your credit principal = {math.floor(cred_prin)}!')
    overpayment(cred_prin, mon_pay, n_per)


def overpayment(cred_prin, mon_pay, n_per):
    overpay = mon_pay * n_per - cred_prin
    print(f'Overpayment = {math.ceil(overpay)}')


def differential(cred_prin, n_per, cred_inte):
    total = 0
    interest_rate = cred_inte / (12 * 100)
    diff = lambda m: math.ceil((cred_prin / n_per) + interest_rate * (cred_prin - (cred_prin * (m - 1)) / n_per))
    for j in range(1, n_per + 1):
        total += diff(j)
        print(f'Month {j}: paid out {diff(j)}')
    print(f'\nOverpayment = {math.ceil(total - cred_prin)}')


# WAS USED BEFORE IMPLEMENTING ARGS
# def main():
#     command = input('''What do you want to calculat?
# type "n" for the count of months,
# type "a" for the annuity monthly payments,
# type "p" for credit principal:
# ''')
#
#     if command == 'n':
#         credit_princial = int(input('Enter credit principal:\n'))
#         monthly_payment = float(input('Enter monthly payment:\n'))
#         credit_interest = float(input('Enter credit interest:\n'))
#         count_months(credit_princial, monthly_payment, credit_interest)
#
#     if command == 'a':
#         credit_princial = float(input('Enter credit principal:\n'))
#         count_periods = int(input('Enter count of periods:\n'))
#         credit_interest = float(input('Enter credit interest:\n'))
#         annuity_monthly_payment(credit_princial, count_periods, credit_interest)
#
#     if command == 'p':
#         monthly_payment = float(input('Enter monthly payment:\n'))
#         count_periods = int(input('Enter count of periods:\n'))
#         credit_interest = float(input('Enter credit interest:\n'))
#         credit_principal(monthly_payment, count_periods, credit_interest)
#
#     if command == 'd':
#         credit_princial = float(input('Enter credit principal:\n'))
#         count_periods = int(input('Enter count of periods:\n'))
#         credit_interest = float(input('Enter credit interest:\n'))
#         differential(credit_princial, count_periods, credit_interest)


def raise_error():
    print('Incorrect parameters')


def check_positive(value):
    f_value = float(value)
    if f_value < 0:
        # raise_error()
        return None
    else:
        return f_value


# main()

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str)
parser.add_argument('--payment', type=check_positive)
parser.add_argument('--principal', type=check_positive)
parser.add_argument('--periods', type=check_positive)
parser.add_argument('--interest', type=check_positive)

args = parser.parse_args()
# print(list(map(type, [args.type, args.payment, args.principal, args.periods, args.interest])))
if args.type == 'diff':
    if not args.payment and all([args.principal, args.periods, args.interest]):
        differential(args.principal, int(args.periods), args.interest)
    else:
        raise_error()
elif args.type == 'annuity':
    if sum(list(map(bool, [args.principal, args.payment, args.periods, args.interest]))) >= 3:
        if not args.payment:
            annuity_monthly_payment(args.principal, int(args.periods), args.interest)
        elif not args.principal:
            credit_principal(args.payment, int(args.periods), args.interest)
        elif not args.periods:
            count_months(args.principal, args.payment, args.interest)
    else:
        raise_error()
else:
    raise_error()
