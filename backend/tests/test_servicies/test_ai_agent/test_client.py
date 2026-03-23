from unittest.mock import AsyncMock, Mock, patch

import pytest

from backlog_app.servicies.ai_agent import AIClient


@pytest.mark.asyncio
async def test_translate_success():
    client = AIClient(model="gpt-test")

    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock()
    mock_response.json = Mock(
        return_value={"choices": [{"message": {"content": "Привет мир"}}]}
    )

    with patch.object(client.client, "post", return_value=mock_response) as mock_post:
        result = await client.translate("Hello world")
        assert result == "Привет мир"

        called_payload = mock_post.call_args[1]["json"]
        assert (
            "Translate the following text from English into Russian"
            in called_payload["messages"][0]["content"]
        )
        assert "Hello world" in called_payload["messages"][0]["content"]


@pytest.mark.asyncio
async def test_translate_http_error():
    client = AIClient(model="gpt-test")

    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(side_effect=Exception("HTTP Error"))
    mock_response.json = AsyncMock(return_value={})

    with patch.object(client.client, "post", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            await client.translate("Hello world")
