import random
import smtplib
from email.mime.text import MIMEText

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp):
    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = "your_email@example.com"
    msg['To'] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your_email@example.com", "your_password_here")
    server.send_message(msg)
    server.quit()
