import math
from babel.numbers import format_currency

def format_numbers(number):
    """Format results to look like $"""

    formatted_number = format_currency(number, 'USD', locale='en_US')
    return formatted_number

def calc_property_taxes(zestimate):
    """Return estimate of property taxes based on home value"""

    # property_taxes = format_numbers(zestimate * .001)
    property_taxes = (zestimate * .001)
    return property_taxes


def calc_ho_ins(zestimate):
    """Return estimate of homeowners insurance based on home value and rules of thumb"""

    # ho_ins = format_numbers((zestimate/1000) * 3.5)
    ho_ins = (zestimate/1000) * 3.5
    return ho_ins


def calc_mortgage(zestimate, downpayment):

    mort_bal = int(zestimate - downpayment)

    # Number of periodic payments (12 payments a year over 30 years)
    n_years = 12 * 30

    # Interest rate (since calculating the monthly payment, divide by 12)
    int_rate = 4.5 / (100 * 12)

    payment = mort_bal * \
            (int_rate/(1-math.pow((1 + int_rate), (-n_years))))
    # payment = format_numbers(payment)
    # NEED TO SEE IF CAN ROUND MORE ACCURATELY 

    # NOTE: CHECK PAYMENT AMOUNT --> THIS SEEMS TOO HIGH!!! 

    return payment


def calc_mo_salary(salary):
    """ Return monthly salary when given annual gross salary"""
    
    mo_salary = salary / 12
    # mo_salary = format_numbers(mo_salary)
    # Can't format here because it messes up the rule_36 function
    return mo_salary


def rule_36(mo_salary, other_debts):
    """ Check if monthly salary is enough for other debts and new mortgage"""

    # mo_salary = int(mo_salary)
    salary_36 = mo_salary * .36
    remaining_budget = ((salary_36) - other_debts)
    # remaining_budget = format_numbers(remaining_budget)


    return remaining_budget

def is_underbudget(remaining_budget, property_taxes, ho_ins, payment):
    """ Check if the payments are affordable based on 36% of budget"""
    mo_property_taxes = property_taxes/12
    mo_ho_ins = ho_ins/12
    piti = mo_property_taxes + mo_ho_ins + payment
    return remaining_budget > piti




