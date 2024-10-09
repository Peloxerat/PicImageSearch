import asyncio

from loguru import logger

from src import EHentai, Network
from src.model import EHentaiResponse
from src.sync import EHentai as EHentaiSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = "../images/test06.jpg"

# Note: EXHentai search requires cookies if to be used
cookies = None

# Use EXHentai search or not, it's recommended to use bool(cookies), i.e. use EXHentai search if cookies is configured
is_ex = False

# Whenever possible, avoid timeouts that return an empty document
timeout = 60


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(client=client, is_ex=is_ex)
        # resp = await ehentai.search(url=url)
        resp = await ehentai.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ehentai = EHentaiSync(
        proxies=proxies,
        is_ex=is_ex,
        cookies=cookies,
        timeout=timeout,
    )
    resp = ehentai.search(url=url)
    # resp = ehentai.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: EHentaiResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].date)

    # It is recommended to use the Compact / Extended page layout, otherwise you will not get tags
    logger.info(resp.raw[0].tags)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()