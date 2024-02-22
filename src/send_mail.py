import base64
import requests
from typing import Dict, Any
import urllib.parse
from configuration import Config

tokenEndpoint = "https://www.googleapis.com/oauth2/v4/token"


def get_access_token(config: Config) -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    config_json = config.email.google_token.model_dump()
    print(f"Access token request JSON:{config_json}")
    body = urllib.parse.urlencode(config_json)
    response = requests.post(tokenEndpoint, headers=headers, data=body)
    response.raise_for_status()  # Raises if the response code is 4XX/5XX
    return response.json().get("access_token")


def format_email(sender: str, recipient: str, subject: str, body: str) -> str:
    return f"To: {recipient}\nFrom: {sender}\nSubject: {handle_unicode(subject)}\n\n{body if body else '.'}\n"


def handle_unicode(string_value: str) -> str:
    encoded = base64.b64encode(string_value.encode()).decode()
    return f"=?utf-8?B?{encoded}?="


def send_email(
    sender: str, recipient: str, subject: str, body: str, config: Config
) -> Dict[str, Any]:
    bearer_token = get_access_token(config)
    authorization_header = f"Bearer {bearer_token}"
    headers = {
        "content-type": "message/rfc822",
        "authorization": authorization_header,
    }
    email_content = format_email(sender, recipient, subject, body)
    gmail_endpoint = f"https://www.googleapis.com/upload/gmail/v1/users/{sender}/messages/send"
    response = requests.post(
        gmail_endpoint,
        headers=headers,
        data=email_content,
    )
    print(f"Sending email with parameters: headers={headers}, body={email_content}")
    response.raise_for_status()
    print(f"Send email result: {response.status_code}, {response.text}")
    return response.json()
