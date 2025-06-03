import sqlite3
import smtplib
import random
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from email.mime.text import MIMEText
from dotenv import load_dotenv
from diabetes import check_input


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

def send_otp(email, otp):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = sender_email
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("Email is missing. Please provide a valid email.", "danger")
            return render_template("signup.html")

        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username already exists
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Username already exists. Please login or use a different username.", "danger")
            return render_template("signup.html")


        # Check if email already exists
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Email already exists. Please login or use a different email.", "danger")
            return render_template("signup.html")

        # Generate OTP and store user temporarily in session
        otp = str(random.randint(100000, 999999))
        session["temp_user"] = {
            "email": email,
            "username": username,
            "password": password,
            "otp": otp
        }
        print("Email submitted:", email)
        send_otp(email, otp)
        return render_template("verify.html")

    return render_template("signup.html")


@app.route("/verify", methods=["POST"])
def verify():
    entered_otp = request.form["otp"]
    if "temp_user" not in session:
        flash("Session expired. Try again.")
        return redirect("/signup")
    if session["temp_user"]["otp"] == entered_otp:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, username TEXT, password TEXT)")
        c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", 
                  (session["temp_user"]["email"], session["temp_user"]["username"], session["temp_user"]["password"]))
        conn.commit()
        conn.close()
        session.pop("temp_user", None)
        flash("Signup successful. Please log in.")
        return redirect("/login")
    else:
        flash("Incorrect OTP. Please try again.")
        return render_template("verify.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        if result and result[0] == password:
            session["user"] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials")
    return render_template("login.html")
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# ---- MAIN PAGE (Protected) ----

@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get("user") is None:
        return redirect(url_for('login'))

    result = ""
    if request.method == 'POST':
        try:
            input_data = {
                'Pregnancies': float(request.form['Pregnancies']),
                'Glucose': float(request.form['Glucose']),
                'BloodPressure': float(request.form['BloodPressure']),
                'SkinThickness': float(request.form['SkinThickness']),
                'Insulin': float(request.form['Insulin']),
                'BMI': float(request.form['BMI']),
                'DiabetesPedigreeFunction': float(request.form['DiabetesPedigreeFunction']),
                'Age': float(request.form['Age']),
            }
            result = check_input(input_data)
        except:
            result = "Invalid input. Please enter valid numeric values."
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)