import httpx
import logging

logger = logging.getLogger(__name__)


async def get_external_quote():
    """Получает случайную цитату из внешнего API ZenQuotes."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://zenquotes.io/api/random")

            if response.status_code != 200:
                logger.error(f"Внешний API вернул статус {response.status_code}")
                return None

            data = response.json()

            # ZenQuotes возвращает список с одним объектом:
            # [{"q": "...", "a": "...", ...}]
            if not isinstance(data, list) or not data:
                logger.error(f"Неожиданный формат ответа внешнего API: {data}")
                return None

            quote_item = data[0]

            quote_text = quote_item.get("q")
            quote_author = quote_item.get("a")

            if not quote_text or not quote_author:
                logger.error(f"В ответе нет q/a: {quote_item}")
                return None

            return {
                "quote": quote_text,
                "author": quote_author
            }

    except Exception as e:
        logger.error(f"Ошибка внешнего API: {e}")
        return None