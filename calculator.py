import math

def calc_property_taxes(zestimate):
    """Return estimate of property taxes based on home value"""

    property_taxes = int(zestimate * .001)
    return property_taxes


def calc_ho_ins(zestimate):
    """Return estimate of homeowners insurance based on home value and rules of thumb"""

    ho_ins = int((zestimate/1000) * 3.5)
    return ho_ins


def calc_mortgage(zestimate, downpayment):

    mort_bal = int(zestimate - downpayment)

    # Number of periodic payments (12 payments a year over 30 years)
    n_years = 12 * 30

    # Interest rate (since calculating the monthly payment, divide by 12)
    int_rate = 4.5 / (100 * 12)

    payment = mort_bal * \
            (int_rate/(1-math.pow((1 + int_rate), (-n_years))))
    payment = int(payment)
    # NEED TO SEE IF CAN ROUND MORE ACCURATELY 

    # NOTE: CHECK PAYMENT AMOUNT --> THIS SEEMS TOO HIGH!!! 

    return payment


def calc_mo_salary(salary):
    """ Return monthly salary when given annual gross salary"""

    mo_salary = salary / 12 
    return mo_salary


def rule_36(mo_salary, other_debts):
    """ Check if monthly salary is enough for other debts and new mortgage"""

    salary_36 = mo_salary * .36
    remaining_budget = salary_36 - other_debts

    # if remaining_budget > mort_pay:
    #     print("You can afford this home!")
    # else:
    #     print("You are too poor, fool!")

    return remaining_budget
