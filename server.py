from pprint import pformat
import os
import requests

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
from flask_debugtoolbar import DebugToolbarExtension

import xmltodict
from calculator import * 

from model import User, connect_to_db, db


app = Flask(__name__)
# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'


@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("homepage.html")


@app.route("/userinfo", methods=["GET"])
def enter_userinfo():
    """Show form for user to enter information"""

    return render_template("userinfo.html")


@app.route("/userinfo", methods=["POST"])
def show_userinfo():

    email = request.form.get('email')
    password = request.form.get('password')
    salary = request.form.get('salary')
    downpayment = request.form.get('downpayment')
    debts = request.form.get('debts')

    if User.query.filter(User.email==email).first() == None:
        user = User(email=email, password=password, salary=salary, downpayment=downpayment, other_debts=debts)

        db.session.add(user)
        db.session.commit()
    else:
        flash("This user already exists")

    return redirect("/")

# @app.route("/show-userprofile")
# def show_userprofile():
#     """Display the user info that was entered"""

#     salary = request.args.get('query')
#     downpayment = request.args.get('downpayment')
#     debts = request.args.get('debts')

#     # Need to store in database

#     return render_template("show-userprofile.html",
#                             salary=salary,
#                             downpayment=downpayment,
#                             debts=debts)


@app.route("/login", methods=["GET"])
def login_form():

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login_process():

    email = request.form.get('email')
    password = request.form.get('password')

    user_query = User.query.filter(User.email == email, User.password == password).first()

    if user_query != None: 
        session["username"] = email
        flash('Logged in')
        user_id = user_query.user_id
        return redirect("/")
    else: 
        flash('Username and password do not match.')
        return redirect("/login")


@app.route("/logout")
def logout_process():
        session.pop("username")
        return redirect("/")


@app.route("/searchhome")
def search_home_form():

    return render_template("search-home.html")


@app.route("/displayhome")
def display_home():
    """Display home information page"""

    address = request.args.get('address')
    citystatezip = request.args.get('citystatezip')

    url = 'http://www.zillow.com/webservice/GetSearchResults.htm'

    parameters = {'zws-id': os.environ.get("ZILLOW_ID"),
                  'address': address,
                  'citystatezip': citystatezip}


    response = requests.get(url, params=parameters)

    data = response.text
    new_dict = xmltodict.parse(data)

    zest = new_dict['SearchResults:searchresults']['response']['results']['result']['zestimate']['amount']['#text']
    zestimate = int(zest)


    #NEED TO CHANGE DOWNPAYMENT/SALARY  
    if "username" in session: 
        email = session["username"]

        user = User.query.filter(User.email == email).first()
        user_id = user.user_id

        downpayment = user.downpayment
        salary = user.salary
        other_debts = user.other_debts


    else: 
        downpayment = 0
        salary = 200000
        other_debts = 0


    property_taxes = calc_property_taxes(zestimate)
    ho_ins = calc_ho_ins(zestimate)
    mort_pay = calc_mortgage(zestimate, downpayment)
    mo_salary = calc_mo_salary(salary)
    remaining_budget = rule_36(mo_salary, other_debts)

    print("CHECK THESE NUMBERS!!!!!")
    print(mort_pay)

    # Had to format mo_salary here because it kept messing up remaining_budget
    mo_salary = format_numbers(mo_salary)
    # Same with zestimate 
    zest = format_numbers(zest)
    # Test for jinja if statement
    budget = remaining_budget
    remaining_budget = format_numbers(remaining_budget)

    mort = mort_pay
    mort_pay = format_numbers(mort_pay)

    # Tested with booleans, and found out that test2bool returns false, when it should return TRUE!
    # For user tree@tree.com, who is too poor for the home 
    # It looks like it has something to do with the formatting (whether its in dollars or left as an int)
    # Need to refactor to make all the formatting numbers cleaner as it's split up over files.... 
    test_bool = budget < mort
    test2_bool = remaining_budget < mort_pay 
    print("BUDGET < MORT: ", test_bool)
    print("remaining < mort pay: ", test2_bool)


    return render_template("display-home.html",
                            data = pformat(data),
                            zest=zest,
                            property_taxes=property_taxes,
                            ho_ins=ho_ins,
                            mort_pay=mort_pay,
                            mo_salary=mo_salary,
                            remaining_budget=remaining_budget,
                            budget=budget,
                            mort=mort)


@app.route("/searchregion")
def search_region_form():

    return render_template("search-region.html")


@app.route("/displayregion")
def display_region():
    """Display region information page"""

    city = request.args.get('city')
    state = request.args.get('state')
    childtype = "neighborhood"

    url = 'http://www.zillow.com/webservice/GetRegionChildren.htm'

    parameters = {'zws-id': os.environ.get("ZILLOW_ID"),
                  'state': state,
                  'city': city,
                  'childtype': childtype}

    response = requests.get(url, params=parameters)

    data = response.text
    order_dict = xmltodict.parse(data, dict_constructor=dict)

    region_list = order_dict['RegionChildren:regionchildren']['response']['list']['region']


    print(region_list)

    return render_template("display-region.html", region_list=region_list)



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")


