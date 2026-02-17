import logging
import uuid
from typing import TYPE_CHECKING, Optional

from fastapi_users import BaseUserManager, UUIDIDMixin

from backlog_app.servicies.mailing import format_seconds_for_email
from backlog_app.config import settings
from backlog_app.models import User
from backlog_app.tasks import email_task

if TYPE_CHECKING:
    from fastapi import Request, Response

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token_db.reset_password_token_secret
    verification_token_secret = settings.access_token_db.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        logger.info("User <%s> has registered.", user.id)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.debug(
            "Verification requested for user <%s>. Verification token: %s",
            user.id,
            token,
        )

        origin = request.headers.get("origin") or settings.FRONTEND_URL
        logger.debug("origin url: %s", origin)

        verification_link = f"{origin}/verify?token={token}"
        await email_task.send_verification_email.kiq(
            user_email=user.email,
            verification_link=verification_link,
        )

    async def on_after_verify(self, user: User, request: Optional["Request"] = None):
        logger.warning("User <%s> has been verified", user.id)

        await email_task.send_email_confirmed.kiq(
            user_email=user.email,
        )

    async def on_after_login(
        self,
        user: User,
        request: Optional["Request"] = None,
        response: Optional["Response"] | None = None,
    ) -> None:
        logger.warning("User <%s> has logged in", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.debug(
            "User <%s> has forgot their password. Reset token: %s, lifetime: %s",
            user.id,
            token,
            self.reset_password_token_lifetime_seconds,
        )
        origin = request.headers.get("origin") or settings.FRONTEND_URL
        reset_link = f"{origin}/forgot-password?token={token}"
        token_lifetime = format_seconds_for_email(
            self.reset_password_token_lifetime_seconds
        )

        await email_task.send_email_forgot_password.kiq(
            user_email=user.email,
            reset_link=reset_link,
            token_lifetime=token_lifetime,
        )

    async def on_after_reset_password(
        self, user: User, request: Optional["Request"] = None
    ) -> None:
        logger.warning("User <%s> successfully changed their password", user.id)

        await email_task.send_email_forgot_password_confirmed.kiq(
            user_email=user.email,
        )
