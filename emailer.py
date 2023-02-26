# Standard library
import os

# Third party
import smtplib
from email.message import EmailMessage

import jinja2
from flask import render_template

PASSWORD = os.environ["MIDAS_EMAIL_PASS"]


def render_jinja_html(template_loc, file_name, **context):

    return (
        jinja2.Environment(loader=jinja2.FileSystemLoader(template_loc + "/"))
        .get_template(file_name)
        .render(context)
    )


def send_email(request_form, email: str, headings: list, results: list):
    """
    Sends email to user about requested insight
    parameters: request_form = html request form as dict
                email: specific user email to send insights to
                headings: insights table headings
                results: insights table row values
    """

    # Unpack necessary parameters
    strategy = request_form["Strategy"].lower()
    length = request_form["Length"]
    interval = request_form["Frequency"]
    market = request_form["Market"]

    # Create html for email
    summary = f"Your requested insights from Midas every {interval} day/s for a {strategy} strategy on \
        the {market} based on the {strategy} over the last {length} months. Your updates can be found below:"

    html = render_jinja_html(
        "templates", "email.html", summary=summary, headings=headings, data=results
    )

    # Create email and define, subject, sender & recipient
    msg = EmailMessage()
    msg["Subject"] = "Midas Insights Notification"
    msg["From"] = "midas.notification@gmail.com"
    msg["To"] = email

    # Send email
    msg.add_alternative(f"""{html}""", subtype="html")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        # Connect encrypt & connect again
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        # Login to mail server
        smtp.login("midas.notification@gmail.com", PASSWORD)
        smtp.send_message(msg)
