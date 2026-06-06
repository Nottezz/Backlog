from unittest.mock import AsyncMock, Mock, patch

import pytest

from backlog_app.servicies.ai_agent import AIClient


@pytest.mark.asyncio
async def test_translate_success():
    client = AIClient(model="gpt-test")

    mock_response = Mock()
    mock_response.choices = [
        Mock(
            message=Mock(
                content="Привет мир",
            )
        )
    ]

    with patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_response,
    ) as mock_create:
        result = await client.translate("Hello world")

        assert result == "Привет мир"

        kwargs = mock_create.call_args.kwargs

        assert kwargs["model"] == "gpt-test"
        assert kwargs["messages"][1]["content"] == "Hello world"


@pytest.mark.asyncio
async def test_translate_error():
    client = AIClient(model="gpt-test")

    with patch.object(
        client.client.chat.completions,
        "create",
        side_effect=Exception("API Error"),
    ):
        with pytest.raises(Exception, match="API Error"):
            await client.translate("Hello world")
