import base64
import requests
from typing import Dict, Any
import urllib.parse
from configuration import Config

tokenEndpoint = "https://www.googleapis.com/oauth2/v4/token"
access_token_headers = {"Content-Type": "application/x-www-form-urlencoded"}


def get_access_token(config: Config) -> str:
    config_json = config.email.google_token.model_dump()
    body = urllib.parse.urlencode(config_json)

    response = requests.post(tokenEndpoint, headers=access_token_headers, data=body)
    response.raise_for_status()

    return response.json().get("access_token")


def format_email(sender: str, recipient: str, subject: str, body: str) -> str:
    encoded_subject = handle_unicode(subject)
    nonempty_body = body if body else "."
    return f"To: {recipient}\nFrom: {sender}\nSubject: {encoded_subject}\n\n{nonempty_body}\n"


def handle_unicode(string_value: str) -> str:
    """
    This function base-64 encodes the subject, which allows unicode characters to be included.
    """
    encoded = base64.b64encode(string_value.encode()).decode()
    return f"=?utf-8?B?{encoded}?="


def send_email(
    sender: str, recipient: str, subject: str, body: str, config: Config
) -> Dict[str, Any]:
    gmail_endpoint = f"https://www.googleapis.com/upload/gmail/v1/users/{sender}/messages/send"

    # The request needs the appropriate auth header
    bearer_token = get_access_token(config)
    authorization_header = f"Bearer {bearer_token}"
    headers = {"content-type": "message/rfc822", "authorization": authorization_header}

    # emails must be formatted in a specific way
    email_content = format_email(sender, recipient, subject, body)

    print(f"Sending email with parameters: headers={headers}, body={email_content}")
    response = requests.post(gmail_endpoint, headers=headers, data=email_content)
    response.raise_for_status()

    print(f"Send email result: {response.status_code}, {response.text}")
    return response.json()
