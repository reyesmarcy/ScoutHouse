from pprint import pformat
import os
import requests

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
from flask_debugtoolbar import DebugToolbarExtension

import xmltodict
from calculator import * 

app = Flask(__name__)
# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'


@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("homepage.html")


@app.route("/userinfo")
def enter_userinfo():
    """Show form for user to enter information"""

    return render_template("userinfo.html")


@app.route("/show-userprofile")
def show_userprofile():
    """Display the user info that was entered"""

    salary = request.args.get('query')
    downpayment = request.args.get('downpayment')
    debts = request.args.get('debts')

    # Need to store in database

    return render_template("show-userprofile.html",
                            salary=salary,
                            downpayment=downpayment,
                            debts=debts)


@app.route("/searchhome")
def search_home_form():

    return render_template("search-home.html")


@app.route("/displayhome")
def display_home():
    """Display home information page"""

    address = request.args.get('address')
    citystatezip = request.args.get('citystatezip')

    url = 'http://www.zillow.com/webservice/GetSearchResults.htm'

    # parameters = {'zws-id' : "X1-ZWz1h23scyeoej_4zss3",
    parameters = {'zws-id': os.environ.get("ZILLOW_ID"),
                  'address': address,
                  'citystatezip': citystatezip}


    response = requests.get(url, params=parameters)

    data = response.text
    new_dict = xmltodict.parse(data)

    zest = new_dict['SearchResults:searchresults']['response']['results']['result']['zestimate']['amount']['#text']

    #NEED TO CHANGE DOWNPAYMENT/SALARY  
    downpayment = 200000
    salary = 200000
    other_debts = 500

    zestimate = int(zest)

    property_taxes = calc_property_taxes(zestimate)
    ho_ins = calc_ho_ins(zestimate)
    mort_pay = calc_mortgage(zestimate, downpayment)
    mo_salary = calc_mo_salary(salary)
    remaining_budget = rule_36(mo_salary, other_debts)

    return render_template("display-home.html",
                            data = pformat(data),
                            zest=zest,
                            property_taxes=property_taxes,
                            ho_ins=ho_ins,
                            mort_pay=mort_pay,
                            mo_salary=mo_salary,
                            remaining_budget=remaining_budget)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5005)


