import asyncio
from pathlib import Path

from loguru import logger

from PicImageSearch import Network, Yandex
from PicImageSearch.model import YandexResponse
from PicImageSearch.sync import Yandex as YandexSync

proxies = "http://127.0.0.1:1080"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = Path(__file__).parent.parent / "images" / "test06.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        yandex = Yandex(client=client)
        # resp = await yandex.search(url=url)
        resp = await yandex.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    yandex = YandexSync(proxies=proxies)
    resp = yandex.search(url=url)
    # resp = yandex.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: YandexResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].source)
    logger.info(resp.raw[0].content)
    logger.info(resp.raw[0].size)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_async())  # type: ignore
    # test_sync()  # type: ignore
