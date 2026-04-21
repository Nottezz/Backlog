import jsonref
import pytest
import pytest_check as check
from fastapi import status
from jsonschema import Draft202012Validator
from test_api.test_openapi.conftest import get_response_schema


def test_openapi_schema_is_valid(openapi_schema):
    Draft202012Validator.check_schema(openapi_schema)


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        pytest.param(
            {"username": "admin@site.com", "password": "12345678"},
            status.HTTP_200_OK,
            id="success",
        ),
        pytest.param(
            {"username": "admin", "password": "wrong"},
            status.HTTP_400_BAD_REQUEST,
            id="invalid_credentials",
        ),
        pytest.param(
            {"username": "admin"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id="missing_password",
        ),
    ],
)
def test_login_response(openapi_schema, client, payload, expected_status) -> None:
    path = f"/api/auth/login"
    response = client.post(
        path,
        data=payload,
    )

    check.equal(response.status_code, expected_status)

    schema = get_response_schema(
        openapi_schema,
        path=path,
        method="post",
        status_code=expected_status,
    )

    if schema is None:
        return

    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors(response.json()))

    for error in errors:
        check.fail(f"{list(error.path)}: {error.message}")
