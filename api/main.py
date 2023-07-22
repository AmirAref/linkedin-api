from fastapi import FastAPI, Form, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from .Linkedin import LinkedinPost

app = FastAPI()

# config static files and templates
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates('templates')

@app.get('/', response_class=HTMLResponse)
async def root(request : Request):
    # home page
    return templates.TemplateResponse(
        'home.html',
        context={'request':request}
        )

# api for developers
@app.post('/api/')
async def api(url: str = Body(..., embed=True)):
    # get data from linkedin
    post = LinkedinPost(url)
    try:
        # return data
        post.get_post_data()
        data = post.to_dict()
        return data
    except Exception as e:
        return {'status':False, 'message': str(e)}
    
# display data humanize for users
@app.post('/', response_class=HTMLResponse)
async def api(request : Request, url: Annotated[str, Form()]):
    # get data from linkedin
    post = LinkedinPost(url)
    try:
        # return data
        post.get_post_data()
        context = {'request':request, 'status':True,
                   'images':post.images, 'videos':post.videos,
                   'document':post.document,
                   }
    except Exception as e:
        context = {'request':request, 'status':False, 'message': str(e)}
    # response 
    return templates.TemplateResponse('post-details.html', context=context)