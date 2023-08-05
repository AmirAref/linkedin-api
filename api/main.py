from fastapi import FastAPI, Form, Request, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from humanize import naturalsize
from .Linkedin import get_post_data, errors, Post

app = FastAPI(
    title="Linekdin API",
    description="this is a tool to download the videos, pictures, documents, etc of a Linkedin.com post.",
    version="0.1.0",
    docs_url="/documentation",
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# config static files and templates
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates('templates')

# config the jinja2
templates.env.globals.update(humanize_size=naturalsize)

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def root(request : Request):
    # home page
    return templates.TemplateResponse(
        'home.html',
        context={'request':request}
        )

# api for developers
@app.post('/api/')
async def api(url: str = Body(..., embed=True)) -> Post:
    # check url is not empty
    if not url:
        raise HTTPException(422, "url is required.")
    # get data from linkedin
    try:
        # return data
        post = get_post_data(url)
        return post
    except (errors.PageNotFound, errors.PostNotFound) as e:
        error_message = "Post not found maybe the URL is uncorrect or the post is private for a specific group."
        raise HTTPException(status_code=422, detail=error_message)
    except Exception as e:
        # error_message = str(e)
        error_message = "undefined error."
        raise HTTPException(status_code=422, detail=error_message)
    
# display data humanize for users
@app.post('/', response_class=HTMLResponse, include_in_schema=False)
async def form_api(request : Request, url: Annotated[str, Form()]):
    # get data from linkedin
    try:
        # return data
        post = get_post_data(url)
        context = {'request':request, 'status':True,
                   'images':post.images, 'videos':post.videos,
                   'document':post.document,
                   }
    except (errors.PageNotFound, errors.PostNotFound) as e:
        error_message = "Post not found maybe the URL is uncorrect or the post is private for a specific group."
        context = {'request':request, 'status':False, 'message': error_message}
    except Exception as e:
        # error_message = str(e)
        error_message = "undefined error from api"
        context = {'request':request, 'status':False, 'message': error_message}
    # response 
    return templates.TemplateResponse('post-details.html', context=context)