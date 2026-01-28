from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    #todo: Update URL
    tokenUrl="auth/jwt/login")
