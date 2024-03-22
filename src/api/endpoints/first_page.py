from typing import Annotated
from fastapi import APIRouter, Form, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from humanize import naturalsize

from src.utils.logger import get_logger
from src.utils.utils import handle_get_post_data
from src import errors


router = APIRouter(include_in_schema=False)
logger = get_logger("first_page")

templates = Jinja2Templates("src/templates")

# config the jinja2
templates.env.globals.update(humanize_size=naturalsize)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    # home page
    return templates.TemplateResponse("home.html", context={"request": request})


# display data humanize for users
@router.post("/", response_class=HTMLResponse, include_in_schema=False)
async def form_api(request: Request, url: Annotated[str, Form()]):
    # get data from linkedin
    try:
        # return data
        post = await handle_get_post_data(url=url, request=request)
        context = {
            "request": request,
            "status": True,
            "images": post["images"],
            "videos": post["videos"],
            "document": post["document"],
        }
    except (errors.PageNotFound, errors.PostNotFound):
        error_message = "Post not found maybe the URL is uncorrect or the post is private for a specific group."
        context = {"request": request, "status": False, "message": error_message}
    except Exception:
        logger.exception(msg="get post data raised an error!")
        error_message = "undefined error from api"
        context = {"request": request, "status": False, "message": error_message}
    # response
    return templates.TemplateResponse("post-details.html", context=context)
