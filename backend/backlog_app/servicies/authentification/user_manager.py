import logging
import uuid
from typing import TYPE_CHECKING, Optional

from fastapi_users import BaseUserManager, UUIDIDMixin

from backlog_app.config import settings
from backlog_app.models import User
from backlog_app.tasks import email_task

if TYPE_CHECKING:
    from fastapi import Request

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token_db.reset_password_token_secret
    verification_token_secret = settings.access_token_db.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        logger.warning("User %s has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.warning(
            "User %s has forgot their password. Reset token: $s", user.id, token
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.warning(
            "Verification requested for user %s. Verification token: %s", user.id, token
        )

        origin = request.headers.get("origin") or settings.FRONTEND_URL
        logger.debug("origin url: %s", origin)

        verification_link = f"{origin}/verify?token={token}"
        await email_task.send_verification_email.kiq(
            user_email=user.email,
            verification_link=verification_link,
        )

    async def on_after_verify(self, user: User, request: Optional["Request"] = None):
        logger.warning("User %s has been verified", user.id)

        await email_task.send_email_confirmed.kiq(
            user_email=user.email,
        )
