from fastapi_users.authentication import AuthenticationBackend

from backlog_app.servicies.authentification import bearer_transport

from .strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
