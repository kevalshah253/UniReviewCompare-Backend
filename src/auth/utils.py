import random
import smtplib
from email.mime.text import MIMEText
from src.utils.config import Config


def generate_otp():
    return ''.join(random.choices('0123456789', k=6))


def send_otp(email, otp):
    sender_email = Config.SENDER_EMAIL  # Enter your email address
    sender_password = Config.SENDER_PASSWORD   # Enter your email password

    message = MIMEText(f"Your OTP for password reset is: {otp}")
    message['Subject'] = 'Password Reset OTP'
    message['From'] = sender_email
    message['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
