===================================================
``sendgmail``: Tools to send email with Gmail API
===================================================
A simple tool to send email with your Gmail account. When running the command for the first time, it will prompt you to place the credential in the displayed folder. Subsequently, it will ask you to login with your Google account, which will be used to send the email.

Prerequisite: 
*OAuth 2.0 ID* file from *console.google.com* stored in **authfiles** directory as **credential.json**.    


Synopsis
========

Usage: ``sendgmail -s "Example subject" -r "recipient@email.com" "example message text``

For more options and help: ``sendgmail --help``

For use in Python

>>> from sendgmail import access_user, create_message, send_message
>>> user = access_user()
Place credential.json in the following folder:
/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/sendgmail/authfiles
(Press any key to continue)
>>> message = create_message(to = "example@email.com", subject = "example", message_text = "example text")
>>> send_message(user, message)
    
Installation
============
``pip install sendgmail``
