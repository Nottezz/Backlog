import httpx
import jsonref
import pytest

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def openapi_schema():
    response = httpx.get(f"{BASE_URL}/openapi.json")
    response.raise_for_status()

    raw_schema = response.json()

    return jsonref.replace_refs(raw_schema)


def get_response_schema(spec, path, method, status_code):
    response = spec["paths"][path][method]["responses"][str(status_code)]

    content = response.get("content", {})
    json_schema = content.get("application/json")

    if not json_schema:
        return None

    return json_schema["schema"]
