from textwrap import dedent

from jinja2_templates import templates
from taskiq_broker import broker
from mailing.send_email import send_email


@broker.task
async def send_verification_email(
    user_id: str,
    user_email: str,
    verification_token: str,
    verification_link: str,
):
    subject = "Confirm your email for site.com"

    plain_content = dedent(f"""\
        Dear {user_email},

        Please verify your email for site.com at {verification_link}.

        Use this token to verify your email: {verification_token}

        Your site admin,
        2025
""")
    template = templates.get_template("email-verify/verification-request.html")
    context = {
        "user_id": user_id,
        "verification_link": verification_link,
        "verification_token": verification_token,
    }
    html_content = template.render(context=context)

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )



@broker.task
async def send_email_confirmed(
    user_id: str,
    user_email: str,
):
    subject = "Email Confirmed"

    plain_content = dedent(f"""\
Dear {user_email},
Your email has been confirmed.
Your site admin,
        2025""")
    template = templates.get_template("email-verify/email-verified.html")
    context = {
        "user_id": user_id,
        "user_email": user_email,
    }
    html_content = template.render(context=context)

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
