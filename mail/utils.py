import sendgrid
from sendgrid.helpers.mail import Mail

from core.settings import DEFAULT_FROM_EMAIL, SENDGRID_API_KEY


def send_sendgrid_mail(to_emails: [str], subject: str, html_content, from_email: str = DEFAULT_FROM_EMAIL):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    mail = Mail(from_email=from_email, to_emails=to_emails, subject=subject, html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())
