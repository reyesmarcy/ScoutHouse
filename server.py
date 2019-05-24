from pprint import pformat
import os
import requests

from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from flask_debugtoolbar import DebugToolbarExtension

import xmltodict
from calculator import * 
from zillowapi import *


from model import User, connect_to_db, db


app = Flask(__name__)
# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'


app.jinja_env.globals.update(format_numbers=format_numbers,
                            calc_property_taxes=calc_property_taxes,
                            calc_ho_ins=calc_ho_ins,
                            calc_mortgage=calc_mortgage,
                            calc_mo_salary=calc_mo_salary,
                            rule_36=rule_36)

class SearchResults: 

    def __init__(self, results):
        self.zestimate = results['zestimate']['amount']['#text']
        self.links = results['links']
        self.home_details = results['links']['homedetails']
        self.graph_data = results['links']['graphsanddata']
        self.map_this = results['links']['mapthishome']
        self.home_latitude = results['address']['latitude']
        self.home_longitude = results['address']['longitude']

# # class RegionResults:

#     def __init__(self, results):
#         self.region_list = results['region']


class Home:

    def __init__(self, user, zestimate):
        self.property_taxes = calc_property_taxes(zestimate)
        self.ho_ins = calc_ho_ins(zestimate)
        self.mort_pay = calc_mortgage(zestimate, user.downpayment)
        self.mo_salary = calc_mo_salary(user.salary)
        self.remaining_budget = rule_36(self.mo_salary, user.other_debts)

# class Region:
#     def __init__(self, user, zestimate):
#         self.


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


@app.route('/monthly-budget.json')
def monthly_budget_data():
    """Return data about monthly budget"""
    if "username" in session: 
        email = session["username"]

        user = User.query.filter(User.email == email).first()
    other_debts = int(user.other_debts)
    
    zest = 100

    labels = ["Remaining Monthly Income", "Other Monthly Debts", "PITI"]
    data_dict = {
                "labels": [
                    "Remaining Monthly Income",
                    "Other Monthly Debts",
                    "PITI"
                ],
                "datasets": [
                    {
                        # "data": [300, other_debts, zest], 
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ]
                    }]
            }
    return jsonify(data_dict)
    return render_template('display-home.html')


@app.route("/displayhome")
def display_home():
    """Display home information page"""

    address = request.args.get('address')
    citystatezip = request.args.get('citystatezip')

    try:
        results = getSearchResults(address, citystatezip)
    # print("LOOOOOOK AAAAT MEEEEEE")
    # print(results)
        zestimate = int(SearchResults(results).zestimate)

    except requests.exceptions.RequestException as e:
        flash('Please enter a valid address.')
        return redirect("/")


    #NEED TO CHANGE DOWNPAYMENT/SALARY  
    if "username" in session: 
        email = session["username"]

        # Query for user object 
        user = User.query.filter(User.email == email).first()
        user_id = user.user_id

        downpayment = user.downpayment
        salary = user.salary
        other_debts = user.other_debts


    else: 
        downpayment = 0
        salary = 200000
        other_debts = 0

    # Instantiate Home Object
    home = Home(user, zestimate)

    affordable = is_underbudget(home.remaining_budget,
                                home.property_taxes,
                                home.ho_ins, 
                                home.mort_pay)

    mo_salary_left = home.mo_salary

    return render_template("display-home.html",
                            # data = pformat(data),
                            zestimate=format_numbers(zestimate),
                            property_taxes=format_numbers(home.property_taxes),
                            ho_ins=format_numbers(home.ho_ins),
                            mort_pay=format_numbers(home.mort_pay),
                            mo_salary=format_numbers(home.mo_salary),
                            remaining_budget=format_numbers(home.remaining_budget),
                            affordable=affordable,
                            user=user, 
                            rand_var = ((home.ho_ins + home.property_taxes)/12 + home.mort_pay),
                            mo_salary_left=mo_salary_left)

    # except:
    #     flash('Please enter a valid address.')
    #     return redirect("/")
  


@app.route("/searchregion")
def search_region_form():

    return render_template("search-region.html")


@app.route("/displayregion")
def display_region():
    """Display region information page"""

    city = request.args.get('city')
    state = request.args.get('state')
    
    if "username" in session: 
            email = session["username"]

        # Query for user object 
            user = User.query.filter(User.email == email).first()
            user_id = user.user_id

    results = getRegion(city, state)
    # zestimate = int(SearchResults(results).zestimate)

    # try:
    #     region_list = order_dict['RegionChildren:regionchildren']['response']['list']['region']

    # zindex = order_dict['RegionChildren:regionchildren']['response']['list']['region']['#text']

    # for region in region_list:
    #     region_name = region['name']
    #     region_zindex = region.get('zindex', {}).get('#text', 0)
    #     # return region_name, region_zindex
    #     print(region_name,  region_zindex)
    #     print()

    # region_dict = {}

    # for region in region_list:
    #     region['name'] = new_dict['region_name']
    #     region.get('zindex', {}).get('#text', 0) = new_dict['region_zindex']




        # if "username" in session: 
        #     email = session["username"]

        #     user = User.query.filter(User.email == email).first()
        #     user_id = user.user_id

        #     downpayment = user.downpayment
        #     salary = user.salary
        #     other_debts = user.other_debts

        # else: 
        #     downpayment = 0
        #     salary = 200000
        #     other_debts = 0


    # {% for i in range(0, len) %}

    #     <li>{{ region_list.region_name[i] }} : {{ region_list.region_zindex[i] }}</li>


    # {% endfor %}

    # {% for region in region_list %}

    #     {{ region['name'] }} : {{ region.get('zindex', {}).get('#text', 0) }}
    #     <br>

    #     {% if {{ region.get('zindex', {}).get('#text', 0) }} != 0 %}
    #         Neighborhood Average: {{ region.get('zindex', {}).get('#text', 0) }}

    for region in results:
        zindex = region.get('zindex', {}).get('#text', 0)
        home = Home(user, int(zindex))

    return render_template("display-region.html", 
                            region_list=results,
                            downpayment=user.downpayment,
                            salary=user.salary,
                            other_debts=user.other_debts,
                            home=home,
                            zindex=zindex)
# except:
    #     flash('Please enter a valid city.')
    #     return redirect("/")



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")



# {% if session.get('username') %}
        
#             {% if budget > mort %}
#                 You can afford this! :) 
#             {% else: %}
#                 You too poor, fool! 
#             {% endif %}  
#         {% endif %}


