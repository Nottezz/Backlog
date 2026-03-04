from textwrap import dedent

from backlog_app.jinja2_templates import templates
from backlog_app.servicies.mailing.email_sender import send_email
from backlog_app.taskiq_broker import broker


@broker.task
async def send_verification_email(
    user_email: str,
    verification_link: str,
) -> None:
    subject = "Подтверждение регистрации на сайте backlog-movie.ru"

    plain_content = dedent(f"""\
            Здравствуйте!
            Пожалуйста, подтвердите ваш адрес электронной почты на сайте backlog-movie.ru, перейдя по ссылке: {verification_link}

            Администрация backlog-movie.ru
        """)
    template = templates.get_template("email-verify/verification-request.html")
    context = {
        "verification_link": verification_link,
    }
    html_content = template.render(context)

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )


@broker.task
async def send_email_confirmed(
    user_email: str,
    login_link: str,
):
    subject = "Адрес электронной почты успешно подтверждён"

    plain_content = dedent(f"""\
        Здравствуйте!
        Ваш адрес электронной почты успешно подтверждён.

        Администрация backlog-movie.ru""")
    template = templates.get_template("email-verify/email-verified.html")
    context = {
        "login_link": login_link,
    }
    html_content = template.render(context)

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )


@broker.task
async def send_email_forgot_password(
    user_email: str, reset_link: str, token_lifetime: str
):
    subject = "Запрос на сброс пароля на сайте backlog-movie.ru"
    plain_content = dedent(f"""\
            Здравствуйте!
            Мы получили запрос на сброс пароля. Перейдите по ссылке, чтобы задать новый пароль: {reset_link}

            Администрация backlog-movie.ru""")
    template = templates.get_template("email-forgot/password-reset-request.html")
    context = {
        "reset_link": reset_link,
        "expires_in": token_lifetime,
    }
    html_content = template.render(context)

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )


@broker.task
async def send_email_forgot_password_confirmed(
    user_email: str,
):
    subject = "Пароль был успешно изменён"
    plain_content = dedent(f"""\
            Здравствуйте!
            Ваш пароль был успешно изменён.

            Администрация backlog-movie.ru""")
    template = templates.get_template("email-forgot/password-reset-confirmed.html")
    html_content = template.render()

    await send_email(
        recipient=user_email,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
