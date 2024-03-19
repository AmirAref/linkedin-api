from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl
import requests
import json
from .errors import *



    
# functions
def get_post_data(url : str):
    #send request
    response = requests.get(url)
    # check status
    if response.status_code in range(400, 500):
        raise PageNotFound("Page not found error !")
    # parse the response
    soup = BeautifulSoup(response.content, "html.parser")
    
    # check the post section is exists
    post_section = soup.find('article')
    if not post_section:
        raise PostNotFound('post not exists !')
    
    # post text
    post = Post(url=url)
    post.text = post_section.find('p', class_='attributed-text-segment-list__content').text
    
    # get post details
    post_detail = post_section.find('div', class_='main-feed-activity-card__social-actions')
    if post_detail:
        # get count of reactions and comments
        _reactions = post_detail.find(attrs={'data-id':'social-actions__reactions'})
        post.reactions = int(_reactions['data-num-reactions']) if _reactions else 0
        _reactions = post_detail.find(attrs={'data-id':'social-actions__comments'})
        post.comments = int(_reactions['data-num-comments']) if _reactions else 0
        
    # extract the post images
    _image_list = post_section.find('ul', attrs={'class':'feed-images-content'})
    if _image_list:
        post.images = [item['data-delayed-url'] for item in _image_list.find_all('img')]
    
    # extract the document
    _document = post_section.find('iframe', attrs={'data-id':'feed-paginated-document-content'})
    # extarct the images from document 
    if _document:
        _document = json.loads(_document['data-native-document-config'])
        # extract
        _doc_url = requests.get(_document['doc']['url']).json()['transcribedDocumentUrl']
        _doc_title = _document['doc']['title']
        post.document = Document(url=_doc_url, title=_doc_title)
        
    
    # get the video links
    _json_data = post_section.find('video')
    if _json_data:
        _json_data = json.loads(_json_data['data-sources'])
        post.videos = [Video(url=item['src'], bitrate=item['data-bitrate']) for item in _json_data]
        post.videos.sort(key=lambda x:x.bitrate, reverse=True)

    return post

# custom models
class Document(BaseModel):
    url : HttpUrl
    title : str

class Video(BaseModel):
    url : HttpUrl
    bitrate : float

class Post(BaseModel):
    url : HttpUrl
    text : str = None
    reactions : int = 0
    comments : int = 0
    images : list[str] = []
    document : Document | None = None
    videos : list[Video] = []