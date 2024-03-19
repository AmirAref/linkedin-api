from fastapi import APIRouter, Request, Body, HTTPException

from src.utils import handle_get_post_data
from src.linkedin.schemas import Post
from src import errors


router = APIRouter()


# api for developers
@router.post("/api/")
async def api(request: Request, url: str = Body(..., embed=True)) -> Post:
    # check url is not empty
    if not url:
        raise HTTPException(422, "url is required.")
    # get data from linkedin
    try:
        # return data
        post = await handle_get_post_data(url=url, request=request)
        return post
    except (errors.PageNotFound, errors.PostNotFound) as e:
        error_message = "Post not found maybe the URL is uncorrect or the post is private for a specific group."
        raise HTTPException(status_code=422, detail=error_message)
    except Exception:
        # error_message = str(e)
        error_message = "undefined error."
        raise HTTPException(status_code=422, detail=error_message)
