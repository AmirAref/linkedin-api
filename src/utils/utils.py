from fastapi import Request
from src.linkedin.crawler import get_post_data
from src.db.crud import create_download, read_download
from src.utils.logger import get_logger

logger = get_logger("utils")


async def handle_get_post_data(url: str, request: Request) -> object:
    # check cache for data
    logger.debug(f"reading post data from database for url {url}")
    download_cache = await read_download(url=url)
    if download_cache:
        # load from cache
        logger.info("post's data loaded from database.")
        return download_cache.data
    else:
        logger.info(f"scraping data for url {url}")
        # scrape data
        data = get_post_data(url=url).model_dump(mode="json")
        # save to cache
        logger.debug(f"adding post data to database for url {url}")
        await create_download(url=url, data=data, ip_address=request.client.host)
        return data
