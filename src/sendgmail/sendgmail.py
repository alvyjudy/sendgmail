"""Functions for the tool"""
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import click

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly'
         ]

AUTHFILES = os.path.dirname(__file__) + "/authfiles"

def access_user(new_user = False):
    """Authenticates the user and returns an object for accessing
    the gmail functions
    
    When first time being run, an OAuth 2.0 Client ID credential is 
    required to authenticate the application before asking for user
    access.

    If user exists (i.e. authfiles/token.pickle exists), this 
    file is loaded and refreshed if needed.
    
    Set new_user to True to replace currently registered user,
    the token.pickle file under the authfiles will be deleted

    Returned object methods:
    drafts, getProfile, history, labels, messages, settings, 
    stop, threads, watch

    """
    try:
        os.mkdir(AUTHFILES)
    except FileExistsError:
        pass

    if new_user:
        try:
            os.remove(AUTHFILES + "/token.pickle")
        except FileNotFoundError:
            return "No token to delete"
            
    try:
        #open token if exists
        with open(AUTHFILES + '/token.pickle', 'rb') as token:
            creds = pickle.load(token)
        #refresh token if expired
        if creds.expired:             
            creds.refresh(Request())
    except FileNotFoundError:
        #token does not exist, register from client secret

        credential_file = AUTHFILES + "/credentials.json"
        if not os.path.exists(credential_file):
            print("Place credential.json in the following folder:\n{folder}".format(folder = AUTHFILES))
            prompt = input("(Press Enter to continue)")
            
        flow = InstalledAppFlow.from_client_secrets_file(
                credential_file, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(AUTHFILES + '/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service.users()
    

def create_message(to, subject, message_text):
    """Create a message for an email and return a dictionary
    object with its "raw" field containing a base64url encoded 
    string
    {'raw': str}

    Example for MIMEText object
    >>> message = email.mime.text.MIMEText("Hello world")
    >>> message['to'] = 'world'
    >>> message['from'] = 'matrix'
    >>> message['subject'] = 'example'
    >>> message.as_bytes()
    b'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nto: alvy\nto: world\nfrom: matrix\nsubject: example\n\nHello'
    >>> base64.urlsafe_b64encode(message.as_bytes())
    b'Q29udGVudC1UeXBlOiB0ZXh0L3BsYWluOyBjaGFyc2V0PSJ1cy1hc2NpaSIKTUlNRS1WZXJzaW9uOiAxLjAKQ29udGVudC1UcmFuc2Zlci1FbmNvZGluZzogN2JpdAp0bzogYWx2eQp0bzogd29ybGQKZnJvbTogbWF0cml4CnN1YmplY3Q6IGV4YW1wbGUKCkhlbGxv'
    """

    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(email_user, message):
    """Send the message
    email_user represents the object returned by the access_user
    function
    b64coded_message represents the object returned by the
    create_message function"""

    message = email_user.messages().send(
                userId='me', body=message).execute()

@click.command()
@click.option('-s', '--subject', nargs=1, type=str, 
               help="Email subject, required")
@click.option('-r', '--recipient', nargs=1, type=str,
              help="Email recipient, required")
@click.option('--whoami', is_flag=True, 
              help="Display the registered email address and exit")
@click.option('--newprofile', is_flag=True, 
              help="Delete current profile and register new profile")
@click.argument('message', required=False, type = str)
def sendgmail(subject, recipient, message, whoami, newprofile):
    """A simple tool to send email with your Gmail account.
    When running the command for the first time, it will prompt you to place the credential in the displayed folder. Subsequently, it will ask you to login with your Google account, which will be used to send the email.

    Prerequisite: 
    OAuth 2.0 ID file from console.google.com stored in authfiles directory as credential.json.    

    Usage: sendgmail -s "Example subject" -r "recipient@email.com" "example message text"

    MESSAGE: Email body

    """

    if newprofile:
        try:
            os.remove(AUTHFILES + '/token.pickle')
            print("Old token deleted")
        except FileNotFoundError:
            print("No token to delete")

    user = access_user()
    
    user_email = user.getProfile(userId='me').execute()['emailAddress']

    if whoami or newprofile:
        print("The current registered email address is: %s" % user_email)
        return
    
    if subject and recipient and message:
        message_object = create_message(recipient, subject, message)
        send_message(user, message_object) 
        print("Email sent to %s using the email address %s" % \
               (recipient, user_email))
    else:
        print("Please make sure subject, recipient and message are included")
    

