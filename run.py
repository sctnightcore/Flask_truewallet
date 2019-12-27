import requests
import time
import os
from truewallet import *
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

"""
Index
"""
@app.route("/")
def index():
	return redirect(url_for('login'))

"""
Truewallet Login
"""
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		res = RequestLoginOTP(email, password)
		if res:
			if res['code'] == "200":
				session['email'] = email
				session['password'] = password
				session['mobile_number'] = res['data']['mobile_number']
				return redirect(url_for('otp', mobile_number=res['data']['mobile_number'], otp_reference=res['data']['otp_reference']))
			else:
				flash('Invalid email or password. Please try again!', 'danger')
		else:
			return redirect(url_for('login'))

	return render_template("login.html")

"""
Truewallet otp login
"""
@app.route("/otp", methods=['GET', 'POST'])
def otp():
	if request.method == "POST":
		otp_code = request.form['otp_code']
		mobile_number = request.form['mobile_number']
		otp_reference = request.form['otp_reference']
		email = session['email']
		password = session['password']
		res = SubmitLoginOTP(email, password, otp_code, mobile_number, otp_reference)
		if res:
			if res['code'] == "200":
				session['access_token'] = res['data']['access_token']
				session['reference_token'] = res['data']['reference_token']
				session['Full_name'] = "{} {}".format(res['data']['firstname_en'], res['data']['lastname_en'])
				flash('You were successfully logged in', 'success')
				return redirect(url_for('profiles'))
			else:
				flash('Invalid OTP code. Please try again!', 'danger')
		else:
			flash('Please try again!', 'danger')
			return redirect(url_for('otp', mobile_number=mobile_number, otp_reference=otp_reference))

	mobile_number = request.args.get("mobile_number")
	otp_reference = request.args.get("otp_reference")
	return render_template("otp.html", mobile_number=mobile_number, otp_reference=otp_reference)

"""
Truewallet Activities to profiles ? 
"""
@app.route("/profiles", methods=['GET', 'POST'])
def profiles():
	if session['access_token'] != None:
		res = GetTransaction(session['access_token'])
		if res:
			if res['code'] == "UPC-200":
				if res['data']['activities'] != None:
					return render_template("profiles.html", data=res['data']['activities'])
				else:
					flash("Please set new startdate!", 'danger')
			else:
				flash('Please try again!', 'danger')
		else:
			return redirect(url_for('profiles'))
	else:
		return redirect(url_for('index'))


"""
Truewallet logout
"""
@app.route("/logout")
def logout():
	session.pop('email', None)
	session.pop('password', None)
	session.pop('mobile_number', None)
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)