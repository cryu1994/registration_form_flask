from flask import Flask, render_template, request, redirect, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"

@app.route('/')

def main():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    count = 0
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['conf_password'] = request.form['conf_password']
    session['bday'] = request.form['bday']

    if len(request.form['first_name']) < 1:
        flash("First Name must be entered!")
        count+=1
    if len(request.form['last_name']) < 1:
        flash("Last name has to be filed")
        count+= 1
    if len(request.form['email']) < 1:
        flash("Email cannot be empty")
        count+= 1
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        count+= 1
    upper_case = 0
    lower_case = 0
    number = 0
    symbol = 0

    for i in session['password']:
        if i.isupper():
            upper_case += 1
        elif i.islower():
            lower_case += 1
        elif i.isdigit():
            number += 1
        else:
            symbol += 1
    if len(request.form['password']) <= 6:
        flash("Password Too weak")
        count+= 1
    elif upper_case > 0 and lower_case > 0 and number > 0 and symbol > 0:
        flash("Password MUST contians at least one number and one special character!")
        count+= 1
    if len(request.form['password']) != len(request.form['conf_password']):
        flash("password not match")
        count+= 1
    if count < 1:
        return redirect("/result")
    else:
        return redirect('/')

@app.route('/result')
def result():
    return render_template("result.html", bday=session['bday'], first_name=session['first_name'], last_name=session['last_name'], email= session['email'], password=session['password'])
app.run(debug=True)
