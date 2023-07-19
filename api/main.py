from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from .Linkedin import LinkedinPost

app = FastAPI()

# config static files and templates
templates = Jinja2Templates('templates')

@app.get('/', response_class=HTMLResponse)
async def root(request : Request):
    # home page
    return templates.TemplateResponse(
        'home.html',
        context={'request':request}
        )


@app.post('/')
async def api(url: Annotated[str, Form()]):
    # get data from linkedin
    post = LinkedinPost(url)
    try:
        # return data
        post.get_post_data()
        data = post.to_dict()
        return data
    except Exception as e:
        return {'status':False, 'message': str(e)}