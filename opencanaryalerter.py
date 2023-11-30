import json
import time
from mailjet_rest import Client

# Mailjet API credentials. free api at https://app.mailjet.com
MAILJET_API_KEY = 'your_mailjet_api_key'
MAILJET_API_SECRET = 'your_mailjet_api_secret'

# Recipient email and phone number
RECIPIENT_EMAIL = 'email goes here'
PHONE_NUMBER = '1234567890'  # Replace with your AT&T phone number

# AT&T Email-to-SMS Gateway Format. replace this with the gateway you use with your carrier. 
ATT_SMS_GATEWAY = f"{PHONE_NUMBER}@txt.att.net"

# Path to the OpenCanary log file
OPENCANARY_LOG_FILE = '/var/tmp/opencanary.log'

def send_alert(subject, body, to_sms=False):
    recipients = [{"Email": RECIPIENT_EMAIL, "Name": "Recipient Name"}]
    if to_sms:
        recipients.append({"Email": ATT_SMS_GATEWAY, "Name": "Recipient SMS"})

    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "your_email@example.com",  # Replace with your email
                    "Name": "Your Name"
                },
                "To": recipients,
                "Subject": subject,
                "TextPart": body,
            }
        ]
    }
    try:
        result = mailjet.send.create(data=data)
        print(f"Alert sent, status: {result.status_code}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_opencanary_log():
    with open(OPENCANARY_LOG_FILE, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            try:
                log_entry = json.loads(line)
                dst_port = log_entry.get('dst_port', -1)
                username = log_entry.get('logdata', {}).get('USERNAME')

                if dst_port == 22:
                    send_alert("OpenCanary Alert: SSH", f"SSH Alert: {log_entry}", to_sms=True)
                elif dst_port == 21:
                    send_alert("OpenCanary Alert: FTP", f"FTP Alert: {log_entry}", to_sms=True)
                elif dst_port == 80:
                    send_alert("OpenCanary Alert: HTTP", f"HTTP Alert: {log_entry}", to_sms=True)
                elif dst_port == 3306:
                    send_alert("OpenCanary Alert: MySQL", f"MySQL Alert: {log_entry}", to_sms=True)
                elif dst_port == 3389:
                    send_alert("OpenCanary Alert: RDP", f"RDP Alert: {log_entry}", to_sms=True)
                elif username == "nmap":
                    send_alert("OpenCanary Alert: Nmap Portscan", f"Nmap Portscan Alert: {log_entry}", to_sms=True)

            except json.JSONDecodeError:
                pass

check_opencanary_log()
