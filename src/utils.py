from fastapi import Request
from src.linkedin import get_post_data
from src.db.crud import create_download, read_download


async def handle_get_post_data(url: str, request: Request) -> object:
    # check cache for data
    download_cache = await read_download(url=url)
    if download_cache:
        # load from cache
        return download_cache.data
    else:
        # scrape data
        data = get_post_data(url=url).model_dump(mode="json")
        # save to cache
        await create_download(url=url, data=data, ip_address=request.client.host)
        return data
