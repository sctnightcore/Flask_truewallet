import os
from truewallet import Truewallet
from flask import Flask, render_template, flash, redirect, url_for, request, session

tw = Truewallet()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

"""
Index
"""
@app.route("/")
def index():
	if session.get('access_token') is None:
		return redirect(url_for('login'))
	else:
		return redirect(url_for('profiles'))

"""
Truewallet Login
"""
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		res = tw.RequestLoginOTP(email, password)
		if res:
			if res['code'] == "200":
				session['email'] = email
				session['password'] = password
				session['mobile_number'] = res['data']['mobile_number']
				return redirect(url_for('otp', mobile_number=res['data']['mobile_number'], otp_reference=res['data']['otp_reference']))
			else:
				return render_template("login.html", error="Invalid email or password. Please try again!")
		else:
			return render_template("login.html", error="Please try again!")
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
		res = tw.SubmitLoginOTP(otp_code, mobile_number, otp_reference)
		if res:
			if res['code'] == "200":
				session['access_token'] = res['data']['access_token']
				session['reference_token'] = res['data']['reference_token']
				session['Full_name'] = "{} {}".format(res['data']['firstname_en'], res['data']['lastname_en'])
				flash('You were successfully logged in', 'success')
				return redirect(url_for('profiles'))
			else:
				return render_template("otp.html", error="Invalid OTP code. Please try again!", mobile_number=mobile_number, otp_reference=otp_reference)
		else:
			return render_template("otp.html", error="Please try again!", mobile_number=mobile_number, otp_reference=otp_reference)
	if request.args.get('mobile_number') and otp_reference is not None:
		mobile_number = request.args.get("mobile_number")
		otp_reference = request.args.get("otp_reference")
		return render_template("otp.html", mobile_number=mobile_number, otp_reference=otp_reference)
	return redirect(url_for('index'))

"""
Truewallet Activities to profiles ?
"""
@app.route("/profiles", methods=['GET', 'POST'])
def profiles():
	if session.get('access_token') is not None:
		res = tw.GetTransaction(session['access_token'])
		if res:
			print(res)
			# TODO !
			if res['code'] == "UPC-200":
				return render_template("profiles.html", data=res)
			else:
				return render_template("profiles.html", error="Please try again!", data=res)
		else:
			return render_template("profiles", error="Fail for get API!", data=None)
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