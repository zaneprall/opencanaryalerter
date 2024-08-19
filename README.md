# opencanaryalerter
An email alert function for opencanaryd
Overview

This script facilitates real-time monitoring of an OpenCanary honeypot log file to detect unauthorized access attempts and alert via email and SMS using the Mailjet API.
Requirements

    Python 3.x
    mailjet_rest library

# Setup

Install Dependencies:

   bash:

    pip install mailjet_rest

   API Credentials:

    Set your Mailjet API key and secret in the script or use environment variables for enhanced security.


   Recipient Configuration:

    Configure the recipient's email and AT&T phone number for SMS alerts.

   Log File Path:

    Set the path to the OpenCanary log file.

Configuration Variables

    MAILJET_API_KEY: Mailjet API key.
    MAILJET_API_SECRET: Mailjet API secret.
    RECIPIENT_EMAIL: Email address for alerts.
    PHONE_NUMBER: Recipient's phone number for SMS.
    OPENCANARY_LOG_FILE: Path to OpenCanary log file.

